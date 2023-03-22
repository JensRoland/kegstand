import proust

# Structured logging fields: https://awslabs.github.io/aws-lambda-powertools-python/2.9.0/core/logger/#standard-structured-keys
logger = proust.Logger()

api = proust.Resource("/hello")

@api.get()
def hello_world():
    return {"message": "Hello, world!"}

@api.get("/:name")
def greet(params):
    name = params.get("name")
    return {"message": f"Greetings, {name}!"}

@api.post("/:name", auth=True)
def greet_with_data(params, data, authorized_user):
    if not authorized_user["custom:is_moderator"]:
        raise proust.ApiError("You are not a moderator!", 403)
    name = params.get("name")
    msg = data.get("msg", "[n/a]")
    return {"message": f"Ahoy-hoy, {name}! A message for you: {msg}", }
