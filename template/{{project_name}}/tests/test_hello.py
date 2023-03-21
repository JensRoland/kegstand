from api.resources.hello.hello import hello

def test_has_get_endpoint():
    # Look through the hello resource's methods to see if it has a GET endpoint.
    assert any([method["method"] == "GET" for method in hello.methods])
