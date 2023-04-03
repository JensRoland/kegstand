import os
import kegstand

# Create the API
api = kegstand.Api()

# Scan folders and add resources to the API
api.find_and_add_resources(os.path.dirname(os.path.abspath(__file__)))

# Export the API as a single Lambda-compatible handler function
handler = api.export()
