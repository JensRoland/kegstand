import os

def find_resource_modules(source_folder: str) -> list:
    # Look through folder structure and create a list of resource modules found.
    # Expects a folder structure like this:
    #   resources/
    #       [resource_name]/
    #           any.py which exposes a resource object named `api`
    resources = []

    # Look for resources
    resources_dir = os.path.join(source_folder, 'resources')
    if os.path.isdir(resources_dir):
        resources.extend(_resources_from_resources_dir(resources_dir))

    # Look for public resources (open endpoints with no auth)
    public_resources_dir = os.path.join(source_folder, 'public_resources')
    if os.path.isdir(public_resources_dir):
        resources.extend(_resources_from_resources_dir(public_resources_dir, require_auth=False))
    
    return resources


def _resources_from_resources_dir(resources_dir: str, require_auth: bool = True) -> list:
    resources = []
    # Get the resource package name from the folder path
    api_index = resources_dir.rfind('/api/')
    resources_package_name = resources_dir[api_index + 5:].replace('/', '.')

    # Loop over folders in resources_dir and import the resource modules
    for resource_name in os.listdir(resources_dir):
        # Ignore files, only look at folders
        if not os.path.isdir(os.path.join(resources_dir, resource_name)):
            continue
        # Skip special folders
        if resource_name.startswith('.') or resource_name.startswith('__'):
            continue
        resources.append({
            'name': resource_name,
            'module_path': f'api.{resources_package_name}.{resource_name}.any',
            'fromlist': ['any'],
            'require_auth': require_auth
        })
    return resources
