import os
import shutil

import click

from proustcli.cli.config import get_proust_config

@click.command()
@click.argument('project_dir')
def new(project_dir):
    project_name = os.path.basename(project_dir)

    if os.path.exists(project_dir):
        raise click.ClickException(f'Folder {project_name} already exists')

    os.mkdir(project_dir)

    try:
        # create the src/api folder
        src_folder = os.path.join(project_dir, 'src')
        os.mkdir(src_folder)
        api_folder = os.path.join(src_folder, 'api')
        os.mkdir(api_folder)

        # create the api module
        api_init_file = os.path.join(api_folder, '__init__.py')
        with open(api_init_file, 'w') as f:
            f.write('from proust.api import ProustApi\n\n')
            f.write('# Import resources\n')
            f.write('from api.resources.hello import hello\n\n')
            f.write('# Create the API\n')
            f.write('api = ProustApi()\n\n')
            f.write('# Add resources to the API\n')
            f.write('api.add_resource(hello)\n\n')
            f.write('# Export the API as a single Lambda-compatible handler function\n')
            f.write('handler = api.export()\n')

        # create the resources folder
        resources_folder = os.path.join(api_folder, 'resources')
        os.mkdir(resources_folder)

        # Create an empty __init__.py file in the resources folder
        resources_init_file = os.path.join(resources_folder, '__init__.py')
        open(resources_init_file, 'a').close()

        # create the hello resource
        hello_file = os.path.join(resources_folder, 'hello.py')
        with open(hello_file, 'w') as f:
            f.write('from proust.decorators import (\n')
            f.write('    ApiResource\n')
            f.write(')\n\n')
            f.write('hello = ApiResource("hello")\n\n')
            f.write('@hello.get()\n')
            f.write('def hello_world(_params):\n')
            f.write('    return {"message": "Hello, world!"}\n\n')
            f.write('@hello.get("/:name")\n')
            f.write('def greet(params):\n')
            f.write('    name = params.get("name")\n')
            f.write('    return {"message": f"Greetings, {name}!"}\n\n')

            f.write('@hello.post("/:name")\n')
            f.write('def greet_with_data(params, data):\n')
            f.write('    name = params.get("name")\n')
            f.write('    msg = data.get("msg", "[none]")\n')
            f.write('    return {"message": f"Ahoy-hoy, {name}! A message for you: {msg}"}\n')

        # create the tests folder
        tests_folder = os.path.join(project_dir, 'tests')
        os.mkdir(tests_folder)

        # create the test module
        test_file = os.path.join(tests_folder, 'test_hello.py')
        with open(test_file, 'w') as f:
            f.write('from api.resources.hello import hello\n\n')
            f.write('def test_has_get_endpoint():\n')
            f.write('    # Look through the hello resource\'s methods to see if it has a GET endpoint.\n')
            f.write('    assert any([method["method"] == "GET" for method in hello.methods])\n')

        # create the CLI configuration file
        with open(os.path.join(project_dir, 'proust.toml'), 'w') as f:
            f.write('[api]\n')
            f.write('name = "My API"\n')
            f.write('description = "My API description"\n')
            f.write('version = "0.1.0"\n')

        # create the Poetry configuration file
        with open(os.path.join(project_dir, 'pyproject.toml'), 'w') as f:
            f.write('[tool.poetry]\n')
            f.write(f'name = "{project_name}"\n')
            f.write('version = "0.1.0"\n')
            f.write('description = "My API description"\n')
            f.write('authors = ["Your Name <you@example.com>"]\n')
            f.write('license = "MIT"\n\n')
            f.write('[tool.poetry.dependencies]\n')
            f.write('proust = {path = "../proust", develop = true}\n')
            f.write('python = "^3.9"\n\n')
            f.write('[tool.poetry.group.dev.dependencies]\n')
            f.write('proustcli = {path = "../proustcli", develop = true}\n')
            f.write('pytest = "^7.2.2"\n\n')
            f.write('[tool.pytest.ini_options]\n')
            f.write('pythonpath = "src"\n')

        # Create the .gitignore file
        with open(os.path.join(project_dir, '.gitignore'), 'w') as f:
            f.write('.venv\n')
            f.write('*.pyc\n')
            f.write('__pycache__\n')
            f.write('dist\n')
            f.write('build\n')
            f.write('.pytest_cache\n')
            f.write('.coverage\n')
            f.write('.mypy_cache\n')
            f.write('.env\n')
            f.write('.DS_Store\n\n')
            f.write('# CDK asset staging directory\n')
            f.write('.cdk.staging\n')
            f.write('cdk.out\n')


        click.echo(f'Created new Proust project: {project_name}')

    except Exception as e:
        click.echo(f'Error creating project: {e}')
        shutil.rmtree(project_dir)
        raise click.Abort()
