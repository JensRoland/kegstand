#!/usr/bin/env python3
import logging
import os
import sys

import aws_cdk as cdk
from aws_cdk import (
    aws_cognito as cognito,
)

from proustcli.infra.stacks.lambda_rest_api import (
    LambdaRestApi
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

parent_stack_name = config['project']['name'].replace(' ', '-')
parent_stack = cdk.Stack(
    app, parent_stack_name,
    description=f"{config['project']['name']} v.{config['project']['version']}",
    env={'region': region})

# Create stacks
modules = {}

if "cdk" in config:
    logger.info("Creating additional resources [cdk]...")
    # Import the project's infra module
    project_infra_path = os.path.join(project_dir, config['cdk']['path_to_infra'])
    sys.path.append(project_infra_path)
    from main import custom_infra
    custom_infra_config = custom_infra(parent_stack, region)
    modules['custom_infra'] = custom_infra_config

if "api" in config:
    logger.info("Creating stack for [api]...")

    user_pool = cognito.UserPool.from_user_pool_id(parent_stack, "UserPool", config['api']['user_pool_id']) if "user_pool_id" in config['api'] else None

    api_construct_name = config['api']['name'].replace(' ', '-')
    api_construct = LambdaRestApi(parent_stack, api_construct_name, config, user_pool=user_pool)

    # Add custom environment variables if provided
    if "custom_infra" in modules and "environment_variables" in modules['custom_infra']:
        for key, value in modules['custom_infra']['environment_variables'].items():
            api_construct.lambda_function.add_environment(key, value)

    modules['api'] = api_construct

# Finally, we can set custom permissions between stacks if needed
if "cdk" in config:
    from main import permissions
    permissions(parent_stack, **modules)

app.synth()
