import kegstand

api = kegstand.ApiResource("/hello", method_defaults={"auth": kegstand.PublicAccess()})

@api.get()
def hello_world():
    return {"message": "Hello, World!"}

@api.get("/:name")
def greet(params):
    return {"message": f"Greetings, {params.get('name')}!"}
