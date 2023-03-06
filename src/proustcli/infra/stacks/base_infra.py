import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from constructs import Construct


class ApiStack(Stack):
    def __init__(self, scope: Construct, id: str, config: object, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the lambda function
        api_lambda = _lambda.Function(
            self, 'ApiLambda',
            code=_lambda.Code.from_asset(f'{config["project_dir"]}/dist'),
            handler="api.handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            memory_size=256
        )

        # Create the api gateway
        proust_api = apigw.LambdaRestApi(
            self, 'ProustAPI',
            handler=api_lambda,
            proxy=True,
            deploy_options=apigw.StageOptions(
                metrics_enabled=True,
                logging_level=apigw.MethodLoggingLevel.INFO
            )
        )
