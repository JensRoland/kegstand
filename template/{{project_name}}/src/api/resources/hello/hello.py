import logging
from proust.decorators import (
    ApiResource,
    ApiError
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

hello = ApiResource("/hello")

@hello.get()
def hello_world(_params):
    return {"message": "Hello, world!"}

@hello.get("/:name")
def greet(params):
    name = params.get("name")
    return {"message": f"Greetings, {name}!"}

@hello.post("/:name", auth=True)
def greet_with_data(params, data, authorized_user):
    if not authorized_user["custom:is_moderator"]:
        raise ApiError("You are not a moderator!", 403)
    name = params.get("name")
    msg = data.get("msg", "[n/a]")
    return {"message": f"Ahoy-hoy, {name}! A message for you: {msg}", }
