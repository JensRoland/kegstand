import os
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_cognito as cognito
)
from constructs import Construct

from proustcli.utils import find_resource_modules


class CognitoStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.user_pool = cognito.UserPool(
            self, "ProustUserPool",
            self_sign_up_enabled=False,  # Disable self sign up
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=False,
                require_symbols=False
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                locale=cognito.StandardAttribute(
                    required=False,
                    mutable=True
                )
            ),
            custom_attributes={
                "tenant": cognito.StringAttribute(min_len=2, max_len=16, mutable=True),
                "is_moderator": cognito.BooleanAttribute(mutable=True)
            },
            # Allow users to sign in via email or username
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
            ),
            # Make username case insensitive
            sign_in_case_sensitive=False,
        )

        # Domain is required for Cognito to work with OAuth
        self.user_pool.add_domain("ProustCognitoDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="proust-cog"
            )
        )

        self.user_pool_client = cognito.UserPoolClient(
            self, "ProustUserPoolClient",
            user_pool=self.user_pool,
            generate_secret=True,  # Enable the authorization code grant flow
            auth_flows=cognito.AuthFlow(
                admin_user_password=True,
                user_password=True,
                user_srp=True,
                custom=True
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=False,  # Disable the implicit code grant flow
                    client_credentials=False
                ),
                scopes=[cognito.OAuthScope.EMAIL, cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE],
                callback_urls=["https://example.com"],
                logout_urls=["https://example.com/logout"]
            )
        )

class LambdaRestApiStack(Stack):
    def __init__(self, scope: Construct, id: str, config: dict, user_pool, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = apigw.RestApi(
            self, f"{id}-RestApi"
        )

        # Configure the Cognito User Pool authorizer
        self.authorizer = apigw.CognitoUserPoolsAuthorizer(
            self, f"{id}-Authorizer", cognito_user_pools=[user_pool]
        )

        # Endpoint logic Lambda function
        self.lambda_function = lambda_.Function(
            self, f"{id}-Function",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler=config["api"]["entrypoint"],
            code=lambda_.Code.from_asset(f'{config["project_dir"]}/dist/api_src'),
            memory_size=256
        )

        # Create a Proxy+ ANY method for the root resource
        # self.api.root.add_proxy(
        #     default_integration=apigw.LambdaIntegration(self.lambda_function),
        #     default_method_options=apigw.MethodOptions(
        #         authorizer=self.authorizer,  # Apply the authorizer
        #     ),
        # )

        # For each resource, create API Gateway endpoints with the Lambda integration
        for resource in find_resource_modules(f'{config["project_dir"]}/dist/api_src/api'):
            resource_root = self.api.root.add_resource(resource["name"])
            if resource["require_auth"]:
                # Private, auth required endpoints
                resource_root.add_proxy(
                    default_integration=apigw.LambdaIntegration(self.lambda_function),
                    default_method_options=apigw.MethodOptions(
                        authorizer=self.authorizer,  # Apply the authorizer
                    ),
                )
            else:
                # Public, no auth required endpoints
                resource_root.add_proxy(
                    default_integration=apigw.LambdaIntegration(self.lambda_function),
                )
