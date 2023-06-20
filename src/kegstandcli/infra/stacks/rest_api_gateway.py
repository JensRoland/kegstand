import click

from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_solutions_constructs import aws_apigateway_lambda as apigw_lambda
from constructs import Construct

from kegstandcli.utils import hosted_zone_from_domain

MODULE_CONFIG_KEY = "api_gateway"

class RestApiGateway(Construct):
    def __init__(self, scope: Construct, id: str, config: dict, user_pool) -> None:
        super().__init__(scope, id)

        provision_with_authorizer = user_pool is not None

        # Lambda API backend
        default_function_props=lambda_.FunctionProps(
            function_name=f"{id}-DefaultGatewayFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="api.lambda.handler",
            code=lambda_.Code.from_asset(f'{config["project_dir"]}/dist/api_gw_src'),
            memory_size=256,
            tracing=lambda_.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "INFO",
                "POWERTOOLS_LOGGER_SAMPLE_RATE": "1.00", # "0.05",  # Use log level DEBUG for 5% of invocations
                "POWERTOOLS_LOGGER_LOG_EVENT": "true",
                "POWERTOOLS_SERVICE_NAME": f"{id}-DefaultGatewayFunction",
            },
        )

        health_lambda_function = lambda_.Function(
            self, f"{id}-HealthCheckFunction",
            function_name=f"{id}-HealthCheckFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="api.lambda.handler",
            code=lambda_.Code.from_asset(f'{config["project_dir"]}/dist/api_gw_src'),
            memory_size=256,
            tracing=lambda_.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "INFO",
                "POWERTOOLS_LOGGER_SAMPLE_RATE": "1.00", # "0.05",  # Use log level DEBUG for 5% of invocations
                "POWERTOOLS_LOGGER_LOG_EVENT": "true",
                "POWERTOOLS_SERVICE_NAME": f"{id}-HealthCheckFunction",
            },
        )

        # If a custom domain name is specified, we create a Route53 record
        # and add the domain name to the API Gateway
        if "domain_name" in config[MODULE_CONFIG_KEY]:
            # Return an error if domain_certificate_arn is not specified
            if "domain_certificate_arn" not in config[MODULE_CONFIG_KEY]:
                click.ClickException(
                    "Config [api_gateway].domain_certificate_arn must be specified when using a custom domain name."
                )

            # API Gateway w. custom domain name
            api_gateway_props=apigw.LambdaRestApiProps(
                rest_api_name=f"{id}-RestApi",
                handler=health_lambda_function,
                proxy=False,  # Disable default proxy resource
                default_method_options=apigw.MethodOptions(
                    authorization_type=apigw.AuthorizationType.NONE
                ),
                deploy_options=apigw.StageOptions(
                    logging_level=apigw.MethodLoggingLevel.INFO,
                    metrics_enabled=True,
                    tracing_enabled=True,
                ),
                domain_name=apigw.DomainNameOptions(
                    domain_name=config[MODULE_CONFIG_KEY]["domain_name"],
                    certificate=acm.Certificate.from_certificate_arn(
                        self,
                        "ApiCertificate",
                        certificate_arn=config[MODULE_CONFIG_KEY]["domain_certificate_arn"],
                    ),
                ),
            )

            # Official 'ApiGatewayToLambda' AWS Solution Construct
            # https://docs.aws.amazon.com/solutions/latest/constructs/aws-apigateway-lambda.html
            api_gateway_to_lambda = apigw_lambda.ApiGatewayToLambda(
                self,
                f"{id}-ApiGatewayConstruct",
                lambda_function_props=default_function_props,
                api_gateway_props=api_gateway_props,
            )
            api = api_gateway_to_lambda.api_gateway

            # Add the Route53 record for the API subdomain
            hosted_zone = route53.HostedZone.from_lookup(self, "HostedZone", domain_name=hosted_zone_from_domain(config[MODULE_CONFIG_KEY]["domain_name"]))
            route53.ARecord(
                self,
                "ApiSubdomainDnsRecord",
                record_name="api",
                zone=hosted_zone,
                target=route53.RecordTarget.from_alias(targets.ApiGateway(api)),
            )

        else:
            # API Gateway w/o custom domain name
            api_gateway_props=apigw.LambdaRestApiProps(
                rest_api_name=f"{id}-RestApi",
                handler=health_lambda_function,
                proxy=False,  # Disable default proxy resource
                default_method_options=apigw.MethodOptions(
                    authorization_type=apigw.AuthorizationType.NONE
                ),
                deploy_options=apigw.StageOptions(
                    logging_level=apigw.MethodLoggingLevel.INFO,
                    metrics_enabled=True,
                    tracing_enabled=True,
                )
            )

            # Official 'ApiGatewayToLambda' AWS Solution Construct
            # https://docs.aws.amazon.com/solutions/latest/constructs/aws-apigateway-lambda.html
            api_gateway_to_lambda = apigw_lambda.ApiGatewayToLambda(
                self,
                f"{id}-ApiGatewayConstruct",
                lambda_function_props=default_function_props,
                api_gateway_props=api_gateway_props,
            )

        self.api = api_gateway_to_lambda.api_gateway
        self.health_check_function = api_gateway_to_lambda.lambda_function

        self.authorizer = None
        # if provision_with_authorizer:
        #     click.echo("Creating Cognito authorizer for API Gateway...")
        #     self.authorizer = apigw.CognitoUserPoolsAuthorizer(
        #         self, f"{id}-Authorizer", cognito_user_pools=[user_pool]
        #     )
            # Add the authorizer to the API Gateway
            # self.api.root.add_proxy(
            #     default_method_options=apigw.MethodOptions(
            #         authorization_type=apigw.AuthorizationType.COGNITO,
            #         authorizer=self.authorizer,  # Apply the authorizer
            #     ),
            # )

        # For each resource, create API Gateway endpoints with the Lambda integration
        resource_root = self.api.root.add_resource("health")
        # Health endpoint is always public (no auth required)
        resource_root.add_proxy(
            default_integration=apigw.LambdaIntegration(health_lambda_function)
        )

        self.deployment = apigw.Deployment(self, f"{id}-Deployment", api=self.api)
