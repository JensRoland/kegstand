import os

import tomli


def get_kegstand_config(project_dir: str):
    config_file = os.path.join(project_dir, 'kegstand.toml')
    print(f'Loading configuration from {config_file}')
    with open(config_file, "rb") as f:
        config = tomli.load(f)
    config['project_dir'] = project_dir
    config['config_file'] = config_file

    # Set defaults where missing
    config_defaults = {
        'api': {
            'name': 'Untitled API',
            'entrypoint': 'api.handler'
        }
    }
    for section, defaults in config_defaults.items():
        if section not in config:
            config[section] = {}
        for key, default in defaults.items():
            if key not in config[section]:
                config[section][key] = default

    return config
