from proust.decorators import (
    ApiResource
)

hello = ApiResource("hello")

@hello.get()
def hello_world(_params):
    return {"message": "Hello, world!"}

@hello.get("/:name")
def greet(params):
    name = params.get("name")
    return {"message": f"Greetings, {name}!"}

@hello.post("/:name")
def greet_with_data(params, data):
    name = params.get("name")
    msg = data.get("msg", "[none]")
    return {"message": f"Ahoy-hoy, {name}! A message for you: {msg}"}
