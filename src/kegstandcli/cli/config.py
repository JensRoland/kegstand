import os
import re
from pathlib import Path

import click
from tomlkit import loads


def get_kegstand_config(verbose, project_dir: str, config_file: str):
    config_file = os.path.join(project_dir, config_file)
    if verbose:
        click.echo(f"Loading configuration from {config_file}")

    parsed_toml_config = loads(Path(config_file).read_text(encoding="utf-8"))

    # If the config file is pyproject.toml, the config will be under the 'tool.kegstand' key
    if config_file.endswith("pyproject.toml"):
        config = parsed_toml_config.get("tool", {}).get("kegstand", {})
        # Some keys are used from the [tool.poetry] section if not specified in [tool.kegstand]
        properties_from_poetry = ["name", "description", "version"]
        if "project" not in config:
            config["project"] = {}
        for property in properties_from_poetry:
            if property not in config["project"]:
                config["project"][property] = (
                    parsed_toml_config.get("tool", {}).get("poetry", {}).get(property)
                )
    else:
        config = parsed_toml_config

    # Validate that the name follows PEP 508
    name_regex = r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$"
    if not re.match(name_regex, config["project"]["name"], flags=re.IGNORECASE):
        raise click.BadParameter(
            f"Name '{config['project']['name']}' is not following PEP 508 naming conventions."
        )

    config["project_dir"] = project_dir
    config["config_file"] = config_file

    # Set defaults where missing
    config_defaults = {
        "api": {"name": "Untitled API", "entrypoint": "api.lambda.handler"}
    }
    for section, defaults in config_defaults.items():
        if section not in config:
            config[section] = {}
        for key, default in defaults.items():
            if key not in config[section]:
                config[section][key] = default

    return config
