import os

import click

from proustcli.cli.config import get_proust_config

@click.command()
@click.argument('project_name')
def new(project_name):
    if os.path.exists(project_name):
        raise click.ClickException(f'Folder {project_name} already exists')

    os.mkdir(project_name)

    # create the src folder
    src_folder = os.path.join(project_name, 'src')
    os.mkdir(src_folder)

    # create the app module
    app_file = os.path.join(src_folder, 'app.py')
    with open(app_file, 'w') as f:
        f.write('from proust.decorators import api_route\n\n')
        f.write("@api_route('/hello', ['GET'])\n")
        f.write("def hello_world(data):\n")
        f.write("    return {'message': 'Hello, world!'}\n\n")
        f.write("@api_route('/hello', ['POST'])\n")
        f.write("def hello_world(data):\n")
        f.write("    name = data.get('name', 'world')\n")
        f.write("    return {'message': f'Hello, {name}!'}\n")

    # create the init file
    init_file = os.path.join(src_folder, '__init__.py')
    open(init_file, 'a').close()

    # create the tests folder
    tests_folder = os.path.join(project_name, 'tests')
    os.mkdir(tests_folder)

    # create the test module
    test_file = os.path.join(tests_folder, 'test_app.py')
    with open(test_file, 'w') as f:
        f.write('from src.app import hello_world\n\n')
        f.write('def test_hello_world():\n')
        f.write('    data = {}\n')
        f.write('    response = hello_world(data)\n')
        f.write('    assert response["message"] == "Hello, world!"\n')

    # create the CLI configuration file
    with open(os.path.join(project_name, 'proust.toml'), 'w') as f:
        f.write('[api]\n')
        f.write('name = "My API"\n')
        f.write('description = "My API description"\n')
        f.write('lambda_asset = "src.app:hello_world"\n')

    # create the Poetry configuration file
    with open(os.path.join(project_name, 'pyproject.toml'), 'w') as f:
        f.write('[tool.poetry]\n')
        f.write(f'name = "{project_name}"\n')
        f.write('version = "0.1.0"\n')
        f.write('description = "My API description"\n')
        f.write('authors = ["Your Name <you@example.com>"]\n')
        f.write('license = "MIT"\n\n')
        f.write('[tool.poetry.dependencies]\n')
        f.write('proust = {path = "../proust"}\n')
        f.write('python = "^3.9"\n\n')
        f.write('[tool.poetry.group.dev.dependencies]\n')
        f.write('proustcli = {path = "../proustcli"}\n')

    # Create the .gitignore file
    with open(os.path.join(project_name, '.gitignore'), 'w') as f:
        f.write('.venv\n')
        f.write('*.pyc\n')
        f.write('__pycache__\n')
        f.write('dist\n')
        f.write('build\n')
        f.write('.pytest_cache\n')
        f.write('.coverage\n')
        f.write('.mypy_cache\n')
        f.write('.DS_Store\n\n')
        f.write('# CDK asset staging directory\n')
        f.write('.cdk.staging\n')
        f.write('cdk.out\n')


    click.echo(f'Created new Proust project: {project_name}')
