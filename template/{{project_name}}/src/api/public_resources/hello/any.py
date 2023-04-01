import proust

api = proust.Resource("/hello")

@api.get()
def hello_world():
    return {"message": "Hello, World!"}

@api.get("/:name")
def greet(params):
    return {"message": f"Greetings, {params.get('name')}!"}
