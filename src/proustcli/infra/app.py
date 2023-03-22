#!/usr/bin/env python3
import logging
import os
import sys

import aws_cdk as cdk

from proustcli.infra.stacks.lambda_rest_api import (
    CognitoStack,
    LambdaRestApiStack
)
from proustcli.cli.config import get_proust_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = cdk.App()

# Get the passed context
region = app.node.try_get_context('region')
project_dir = app.node.try_get_context('project_dir')

# Get the Proust config
config = get_proust_config(project_dir)

logger.info(f"Creating app with config: {config}")


# Create stacks
modules = {}

if "cdk" in config:
    logger.info(f"Creating additional resources [cdk]...")
    # Import the project's infra module
    project_infra_path = os.path.join(project_dir, config['cdk']['path_to_infra'])
    sys.path.append(project_infra_path)
    from main import custom_infra
    custom_infra_config = custom_infra(app, region)
    modules['custom_infra'] = custom_infra_config

if "api" in config:
    logger.info(f"Creating stack for [api] '{config['api']['name']}'...")
    # Use the api name from the config as the stack name
    api_stack_name = config['api']['name'].replace(' ', '-')
    cognito_stack = CognitoStack(app, "proust-auth", env={'region': region})
    api_stack = LambdaRestApiStack(app, api_stack_name, config, user_pool=cognito_stack.user_pool, env={'region': region})

    # Add custom environment variables if provided
    if "environment_variables" in modules['custom_infra']:
        for key, value in modules['custom_infra']['environment_variables'].items():
            api_stack.lambda_function.add_environment(key, value)

    modules['api'] = api_stack



# Finally, we can set custom permissions between stacks if needed
if "cdk" in config:
    from main import permissions
    permissions(app, **modules)

app.synth()
