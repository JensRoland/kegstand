from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_cognito as cognito,
)
from aws_solutions_constructs import aws_apigateway_lambda as apigw_lambda
from constructs import Construct

from kegstandcli.utils import find_resource_modules

class LambdaRestApi(Construct):
    def __init__(self, scope: Construct, id: str, config: dict, user_pool) -> None:
        super().__init__(scope, id)

        provision_with_authorizer = user_pool is not None

        # Find all the resource modules in the API source directory
        resource_modules = find_resource_modules(f'{config["project_dir"]}/dist/api_src/api')

        powertools_layer_package = "AWSLambdaPowertoolsPythonV2:25"  # For ARM architecture, use AWSLambdaPowertoolsPythonV2-Arm64:25

        # Official AWS Solution Construct: https://docs.aws.amazon.com/solutions/latest/constructs/aws-apigateway-lambda.html
        api_gateway_to_lambda = apigw_lambda.ApiGatewayToLambda(
            self, f"{id}-ApiGatewayConstruct",
            lambda_function_props=lambda_.FunctionProps(
                function_name=f"{id}-Function",
                runtime=lambda_.Runtime.PYTHON_3_9,
                handler=config["api"]["entrypoint"],
                code=lambda_.Code.from_asset(f'{config["project_dir"]}/dist/api_src'),
                layers=[  # Lambda Powertools: https://awslabs.github.io/aws-lambda-powertools-python/2.4.0/
                    lambda_.LayerVersion.from_layer_version_arn(
                        self, "PowertoolsLayer",
                        layer_version_arn=f"arn:aws:lambda:{Stack.of(self).region}:017000801446:layer:{powertools_layer_package}",
                    )
                ],
                memory_size=256,
                tracing=lambda_.Tracing.ACTIVE,
                environment={
                    "LOG_LEVEL": "INFO",
                    "POWERTOOLS_LOGGER_SAMPLE_RATE": "0.1",
                    "POWERTOOLS_LOGGER_LOG_EVENT": "true",
                    "POWERTOOLS_SERVICE_NAME": "authie-token-function",
                },
            ),
            api_gateway_props=apigw.RestApiProps(
                rest_api_name=f"{id}-RestApi",
                default_method_options=apigw.MethodOptions(authorization_type=apigw.AuthorizationType.NONE),
                deploy_options=apigw.StageOptions(
                    logging_level=apigw.MethodLoggingLevel.INFO,
                    metrics_enabled=True,
                    tracing_enabled=True,
                ),
            ),
        )
        self.api = api_gateway_to_lambda.api_gateway
        self.lambda_function = api_gateway_to_lambda.lambda_function

        self.authorizer = None
        if provision_with_authorizer:
            self.authorizer = apigw.CognitoUserPoolsAuthorizer(
                self, f"{id}-Authorizer", cognito_user_pools=[user_pool]
            )

        # For each resource, create API Gateway endpoints with the Lambda integration
        for resource in resource_modules:
            resource_root = self.api.root.add_resource(resource["name"])
            if resource["require_auth"]:
                # TODO: add a nice error message if a user pool was not passed in (authorizer is None)
                # Private, auth required endpoints
                resource_root.add_proxy(
                    default_integration=apigw.LambdaIntegration(self.lambda_function),
                    default_method_options=apigw.MethodOptions(
                        authorization_type=apigw.AuthorizationType.COGNITO,
                        authorizer=self.authorizer,  # Apply the authorizer
                    ),
                )
            else:
                # Public, no auth required endpoints, public endpoints
                resource_root.add_proxy(
                    default_integration=apigw.LambdaIntegration(self.lambda_function)
                )

        self.deployment = apigw.Deployment(self, f"{id}-Deployment", api=self.api)
