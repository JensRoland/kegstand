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
            code=_lambda.Code.from_asset(f'{config["api"]["lambda_asset_path"]}/dist'),
            handler=config["api"]["lambda_asset_handler"],
            runtime=_lambda.Runtime.PYTHON_3_8,
            memory_size=256
        )

        # Create the api gateway
        proust_api = apigw.LambdaRestApi(
            self, 'ProustAPI',
            handler=api_lambda,
            proxy=False,
            deploy_options=apigw.StageOptions(
                metrics_enabled=True,
                logging_level=apigw.MethodLoggingLevel.INFO
            )
        )

        # TODO: Use proxy=True and remove the resource and method creation,
        # this could make everything much simpler.

        # Create a resource and method for the api gateway
        proust_resource = proust_api.root.add_resource('proust')
        method_get = proust_resource.add_method(
            'GET',
            integration=apigw.LambdaIntegration(api_lambda),
            authorization_type=apigw.AuthorizationType.IAM
        )
        method_post = proust_resource.add_method(
            'POST',
            integration=apigw.LambdaIntegration(api_lambda),
            authorization_type=apigw.AuthorizationType.IAM
        )
