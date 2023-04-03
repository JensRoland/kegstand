import os
import click

from kegstandcli.cli.new import new
from kegstandcli.cli.build import build
from kegstandcli.cli.deploy import deploy
from kegstandcli.cli.teardown import teardown

# We pass the project directory to all subcommands via the context
# so they can use it to find the kegstand.toml file
@click.group()
@click.option('--config', default='kegstand.toml', help='Path to Kegstand configuration file.')
@click.pass_context
def kegstandcli(ctx, config):
    """
██   ██ ███████  ██████  ███████ ████████  █████  ███    ██ ██████             
██  ██  ██      ██       ██         ██    ██   ██ ████   ██ ██   ██            
█████   █████   ██   ███ ███████    ██    ███████ ██ ██  ██ ██   ██            
██  ██  ██      ██    ██      ██    ██    ██   ██ ██  ██ ██ ██   ██            
██   ██ ███████  ██████  ███████    ██    ██   ██ ██   ████ ██████             
===================================================================            
The Developer's Toolbelt For Accelerating Mean-Time-To-Party on AWS"""
    project_dir = os.path.abspath(os.path.dirname(config))
    ctx.obj = {'config': os.path.abspath(config),
               'project_dir': project_dir}

for command in [new, build, deploy, teardown]:
    kegstandcli.add_command(command)

if __name__ == '__main__':
    kegstandcli(obj={})
