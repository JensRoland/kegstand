#!/usr/bin/env python3
import os

import aws_cdk as cdk

from proustcli.infra.stacks.base_infra import ApiStack
from proustcli.cli.config import get_proust_config


app = cdk.App()

# Get the passed context
stack_name = app.node.try_get_context('stack_name')
region = app.node.try_get_context('region')
project_dir = app.node.try_get_context('project_dir')

# Get the Proust config
config = get_proust_config(project_dir)

# Create the stack
ApiStack(app, stack_name, config, env={'region': region})

app.synth()
