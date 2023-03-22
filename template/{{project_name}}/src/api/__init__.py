import os
from proust.api import ProustApi

# Create the API
api = ProustApi()

# Scan folders and add resources to the API
api.find_and_add_resources(os.path.dirname(os.path.abspath(__file__)))

# Export the API as a single Lambda-compatible handler function
handler = api.export()
