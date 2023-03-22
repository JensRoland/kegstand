import os
import click

from proustcli.cli.new import new
from proustcli.cli.build import build
from proustcli.cli.deploy import deploy
from proustcli.cli.teardown import teardown

# We pass the project directory to all subcommands via the context
# so they can use it to find the proust.toml file
@click.group()
@click.option('--config', default='proust.toml', help='Path to Proust configuration file.')
@click.pass_context
def proustcli(ctx, config):
    project_dir = os.path.abspath(os.path.dirname(config))
    ctx.obj = {'config': os.path.abspath(config),
               'project_dir': project_dir}

for command in [new, build, deploy, teardown]:
    proustcli.add_command(command)

if __name__ == '__main__':
    proustcli(obj={})
