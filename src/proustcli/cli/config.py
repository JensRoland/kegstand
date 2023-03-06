import os

import tomli


def get_proust_config(project_dir: str):
    config_file = os.path.join(project_dir, 'proust.toml')
    print(f'Loading configuration from {config_file}')
    with open(config_file, "rb") as f:
        config = tomli.load(f)
    config['project_dir'] = project_dir
    config['config_file'] = config_file

    # Split the lambda asset into a path and a file&handler.
    # The format is path.to.module:handler
    # And we need the path "path/to" and the handler "module.handler"
    lambda_asset = config['api']['lambda_asset']
    path, handler = lambda_asset.split(':')
    path_segments = path.split('.')
    config['api']['lambda_asset_handler'] = path_segments.pop() + '.' + handler
    config['api']['lambda_asset_path'] = os.path.join(config['project_dir'], *path_segments)

    return config
