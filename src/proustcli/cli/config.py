import os

import tomli


def get_proust_config(project_dir: str):
    config_file = os.path.join(project_dir, 'proust.toml')
    print(f'Loading configuration from {config_file}')
    with open(config_file, "rb") as f:
        config = tomli.load(f)
    config['project_dir'] = project_dir
    config['config_file'] = config_file

    return config
