from proust.api import ProustApi

# Import resources
from api.resources.hello import hello

# Create the API
api = ProustApi()

# Add resources to the API
api.add_resource(hello)

# Export the API as a single Lambda-compatible handler function
handler = api.export()
