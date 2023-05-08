import os


def find_resource_modules(api_dir: str) -> list:
    # Look through folder structure and create a list of resource modules found.
    # Expects a folder structure like this:
    #   api/
    #       [resource_name].py which exposes a resource object named `api`
    resources = []

    # Loop over folders in api_dir and import the resource modules
    for file_descriptor in os.listdir(api_dir):
        # Ignore folders, only look at files
        if os.path.isdir(os.path.join(api_dir, file_descriptor)):
            continue
        # Skip dotfiles and special files
        if (
            file_descriptor.startswith(".")
            or file_descriptor.startswith("__")
            or file_descriptor == "lambda.py"
        ):
            continue
        resource_name = os.path.splitext(file_descriptor)[0]
        resources.append(
            {
                "name": resource_name,
                "module_path": f"api.{resource_name}",
                "fromlist": [resource_name],
            }
        )
    return resources

def hosted_zone_from_domain(domain: str) -> str:
    return ".".join(domain.split(".")[-2:])
