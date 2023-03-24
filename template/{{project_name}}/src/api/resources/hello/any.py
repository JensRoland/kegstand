import proust

logger = proust.Logger()

api = proust.Resource("/hello")

@api.get()
def hello_world():
    return {"message": "Hello, World!"}

@api.get("/:name")
def greet(params):
    name = params.get("name")
    logger.info(f"Greeting {name} from /hello")
    return {"message": f"Greetings, {name}!"}

@api.post(
    path="/:name",
    auth=proust.Auth.require("custom:is_moderator").to_be("true")
)
def greet_with_data(params, data, claims):
    name = params.get("name")
    msg = data.get("msg", "[n/a]")
    return {"message": f"Ahoy-hoy, {name}! A message for you: {msg}", }
