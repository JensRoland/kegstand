"""REST API backend infrastructure stack."""

from pathlib import Path
from typing import Any

import click
from aws_cdk import CfnOutput, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_lambda as lambda_
from constructs import Construct

from kegstandcli.utils import LambdaRuntime, find_resource_modules

MODULE_CONFIG_KEY = "api"


class RestApiBackend(Construct):
    """Construct for creating a REST API backend with Lambda integration.

    This construct creates a Lambda function and API Gateway endpoints for each resource
    module found in the API source directory. It optionally supports Cognito user pool
    authorization for non-public endpoints.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: dict[str, Any],
        rest_api_gw: apigw.IRestApi,
        user_pool: cognito.IUserPool | None,
    ) -> None:
        """Initialize the REST API backend.

        Args:
            scope: CDK construct scope
            construct_id: Unique identifier for the construct
            config: Project configuration dictionary
            rest_api_gw: API Gateway REST API instance
            user_pool: Optional Cognito user pool for authorization
        """
        super().__init__(scope, construct_id)

        provision_with_authorizer = user_pool is not None

        # Find all the resource modules in the API source directory
        api_src_path = Path(config["project_dir"]) / "build" / "api_src"
        resource_modules = find_resource_modules(str(api_src_path))

        # Output all modules found
        click.echo("API backend: Found the following resource modules:")
        for resource in resource_modules:
            click.echo(f" - Name: {resource['name']}")
            click.echo(f"   Module path: {resource['module_path']}")
            click.echo(f"   Fromlist: {resource['fromlist']}")
            click.echo(f"   Is public: {resource['is_public']}")

        powertools_layer_package = {
            "x86_64": "AWSLambdaPowertoolsPythonV2:25",
            "arm64": "AWSLambdaPowertoolsPythonV2-Arm64:25",
        }["x86_64"]  # TODO: make this configurable

        # Lambda API backend
        self.lambda_function = lambda_.Function(
            self,
            f"{construct_id}-Backend",
            function_name=f"{construct_id}-Function",
            runtime=LambdaRuntime(config[MODULE_CONFIG_KEY]["runtime"]).to_lambda_runtime(),
            handler=config[MODULE_CONFIG_KEY]["entrypoint"],
            code=lambda_.Code.from_asset(str(api_src_path)),
            layers=[  # See Lambda Powertools: https://awslabs.github.io/aws-lambda-powertools-python/2.4.0/
                lambda_.LayerVersion.from_layer_version_arn(
                    self,
                    "PowertoolsLayer",
                    layer_version_arn=(
                        f"arn:aws:lambda:{Stack.of(self).region}:017000801446:layer:"
                        f"{powertools_layer_package}"
                    ),
                )
            ],
            memory_size=256,
            tracing=lambda_.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "INFO",
                "POWERTOOLS_LOGGER_SAMPLE_RATE": "1.00",
                "POWERTOOLS_LOGGER_LOG_EVENT": "true",
                "POWERTOOLS_SERVICE_NAME": f"{construct_id}-Function",
            },
        )

        self.authorizer = None
        if provision_with_authorizer:
            click.echo("Creating Cognito authorizer for API...")
            self.authorizer = apigw.CognitoUserPoolsAuthorizer(
                self,
                f"{construct_id}-Authorizer",
                cognito_user_pools=[user_pool],  # type: ignore
            )

        # For each resource, create API Gateway endpoints with the Lambda integration
        for resource in resource_modules:
            if provision_with_authorizer and not resource["is_public"]:
                # Private, auth required endpoints
                resource_root = rest_api_gw.root.add_resource(
                    resource["name"],
                    default_integration=apigw.LambdaIntegration(self.lambda_function),
                    default_method_options=apigw.MethodOptions(
                        authorization_type=apigw.AuthorizationType.COGNITO,
                        authorizer=self.authorizer,  # This applies the authorizer
                    ),
                )
                resource_root.add_method("ANY", apigw.LambdaIntegration(self.lambda_function))
                resource_root.add_proxy()
            else:
                # Public (no auth required) endpoints
                resource_root = rest_api_gw.root.add_resource(
                    resource["name"],
                    default_integration=apigw.LambdaIntegration(self.lambda_function),
                )
                resource_root.add_method("ANY", apigw.LambdaIntegration(self.lambda_function))
                resource_root.add_proxy()

            # Add a CfnOutput with the resource URL
            CfnOutput(
                scope,
                f"{resource['name']}Url",
                value=rest_api_gw.url_for_path(resource_root.path),
                description=f"Endpoint URL for the {resource['name']} resource",
            )

        self.deployment = apigw.Deployment(self, f"{construct_id}-Deployment", api=rest_api_gw)
