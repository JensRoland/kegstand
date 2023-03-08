#!/usr/bin/env python3
import logging
import os
import sys

import aws_cdk as cdk

from proustcli.infra.stacks.base_infra import ApiStack
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

if "cdk" in config:
    logger.info(f"Creating additional resources [cdk]...")
    project_infra_path = os.path.join(project_dir, config['cdk']['path_to_infra'])
    sys.path.append(project_infra_path)
    from main import export_stack
    stack_config = export_stack(app)

if "api" in config:
    logger.info(f"Creating stack for [api] '{config['api']['name']}'...")
    # Use the api name from the config as the stack name
    api_stack_name = config['api']['name'].replace(' ', '-')
    ApiStack(app, api_stack_name, config, env={'region': region})

app.synth()
