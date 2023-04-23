<!-- markdownlint-disable line-length -->

# Kegstand documentation

## The configuration file

A Kegstand project folder must contain a Kegstand configuration file. This can be a separate file named `kegstand.toml` (or `.kegstand`), or the configuration can be embedded in an existing `pyproject.toml` file. The Kegstand CLI will automatically detect the correct configuration file and use it.

The Kegstand configuration uses TOML, and it looks like this:

```toml
[project]
name = "My-Service"  # No spaces, must be PEP 508 compliant
version = "0.1.0"

[api]
name = "My Service API"
```

If you are using the `pyproject.toml` file, the Kegstand configuration should be placed under the `[tool.kegstand]` namespace, like this:

```toml
# Note: project keys 'name', 'description' and 'version' are automatically
# inherited from the [tool.poetry] section, so the [tool.kegstand.project]
# section can usually be omitted when using pyproject.toml.

[tool.kegstand.api]
name = "My Service API"
```

For the version numbering we recommend following [Semantic Versioning](https://semver.org/), although this is not strictly enforced by Kegstand.

For a full list of configuration options, see the [Configuration Reference](https://kegstand.dev/docs/configuration-reference) on the Kegstand website.<!-- markdown-link-check-disable-line -->

## Developing with Kegstand

### Example 1 &mdash; Creating a simple API

Creating a public REST API endpoint is as easy as editing the `any.py` file in the correct resource subfolder. Here's an example of a simple API that greets a user by name:

```python
import kegstand

api = kegstand.ApiResource("/hello")

@api.get("/:name", auth=kegstand.PublicAccess())
def greet(params):
    return {
        "message": f"Hello, {params.get('name')}!"
    }
```

Deploying it takes just a single command:

```shell
> keg deploy
```

This will automatically deploy the new endpoint to AWS, and it should be ready to take requests in a few minutes. Under the hood, Kegstand uses CDK, so all the corresponding cloud resources deploy together as a stack in the AWS Cloudformation console.

To test the endpoint, you simply issue a GET request to the generated endpoint URL, either by opening it in a browser or by using a tool like curl or [HTTPie](https://httpie.org/). For example, using HTTPie:

```shell
> https GET http://<API_ID>.execute-api.<REGION>.amazonaws.com/prod/hello/Beth
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 25
Content-Type: application/json

{
    "message": "Hello, Beth!"
}
```

### Example 2 &mdash; Authorized POST endpoint

This time, we will make a REST API endpoint `/diary/<entry_date>`which lets us POST new entries to an online diary. We will require that the user is authorized and that their email matches `you@example.com` to be allowed to post to the diary.

Creating an authorized API endpoint with Kegstand assumes that you have an existing [Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html) which you can use to generate OAuth 2.0 JWT tokens with the `openid` scope. If you don't already have a user pool, you can set one up in just a few minutes with [Authie](https://github.com/JensRoland/authie), which, by the way, is powered by Kegstand. Yes, this party _definitely_ has a drum circle on the back lawn.<!-- markdown-link-check-disable-line -->

Once you have a Cognito User Pool, add the User Pool ID to the `[tool.kegstand.api]` section of the `pyproject.toml` file:

```toml
[tool.kegstand.api]
name = "My Service API"
user_pool_id = "__USER_POOL_ID__"
```

Then, create a new folder `diary` under `src/api/resources` for our new API resource. The folder structure should now look like this:

```shell
my-service
├── .gitignore                        # Gitignore file
├── pyproject.toml                    # Project configuration
└── src
    └── api
        └── resources
            ├── hello
            │   └── any.py            # Logic for /hello/
            └── diary
                └── any.py            # Logic for /diary/
```

(Remember to sprinkle in some `__init__.py` files until it looks like a Python project.)

In the `api/resources/diary/any.py` file, add the following code:

```python
import kegstand

logger = kegstand.Logger()

api = kegstand.ApiResource("/diary")

@api.post(
    route="/:entry_date",
    auth=kegstand.claim("email").eq("you@example.com")
)
def add_diary_entry(params, data):
    entry_date = params.get("entry_date")
    # Expect a JSON body payload with a "dear_diary" key
    # like so: {"dear_diary": "Today I went to the store..."}
    dear_diary = data.get("dear_diary", "")

    # Store the diary entry in a database here...

    logger.info("Added diary entry for %s: %s characters", entry_date, len(dear_diary))

    return {
        "message": "OK"
    }
```

The `auth` parameter in the `@api.post` decorator is a Kegstand expression that checks the JWT token for the `email` claim and compares it to the string `"you@example.com"`. If the claim is not present, or if the claim does not match the string, the endpoint will return a 401 Unauthorized response.

Run `keg deploy` to deploy the new endpoint to AWS, and the command will output the URL for the new endpoint.

To test this endpoint, you will first need to obtain a JWT token for the user you want to authorize, and when you issue the POST request, include an authorization header with the JWT's `id_token`.

Using the [HTTPie](https://httpie.org/) commandline tool, you can issue a POST request with Bearer Auth like this:

```shell
> https -A bearer -a <ID_TOKEN> POST http://<API_ID>.execute-api.<REGION>.amazonaws.com/prod/diary/2023-02-13
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 25
Content-Type: application/json

{
    "message": "OK"
}
```

### Example 3 &mdash; Adding custom AWS resources

When most popular serverless productivity tools call it a night, Kegstand taps the next keg and kicks the party into high gear. Kegstand is built on top of [AWS CDK](https://aws.amazon.com/cdk/) and gives you the full power of CDK with familiar Python code to deploy any AWS resource you want, including databases, S3 buckets, DynamoDB tables, GPU clusters, or anything else you might need. Kegstand's `keg deploy` command deploys your custom infrastructure together with any Kegstand APIs you define, and even makes it easy to set up IAM permissions between them.

...(more to come)

## The Philosophy

- Convention over configuration: As long as the conventions are reasonable, easy to learn, and increase developer velocity, the benefits outweigh the resulting decrease in configurability.
- Opinionated and domain-optimized is better than agnostic but generic. An opinionated solution that works today is better than a tech-agnostic solution that you have to spend weeks configuring.
- Frameworks should make the simple things easy, and the hard things possible. And if a user needs to do one of the hard things, that shouldn't suddenly blow up the easy things they already did.
- If an input is required, but 90% of the time people will use a certain value, make it a default. Configurability is great, but pragmatic defaults are better.
- Repos should not contain files they don't own. Ask yourself: "Are the maintainers of this repo allowed to fundamentally alter this file?" If the answer is "no" &mdash; maybe the file contains company-mandated linting rules or standard infrastructure components which should only be changed by a central team &mdash; then the file doesn't belong there.
- For solved problems, like how to build and deploy a REST API endpoint, a developer should be able to go from zero to a running solution in 10 minutes or less. And if it took them 15 minutes, those extra 5 minutes better have gone into application logic, not repeating the same tedious boilerplate configuration.
- Just because a service has to be built quickly on a deadline, that doesn't mean it has to be unreliable, unobservable, or insecure.

## Comparison to other tools

Why not just use SAM? Or Serverless Framework? Or Chalice? Or...? There are a lot of tools out there for building serverless applications, and they all have their strengths and weaknesses. Kegstand might not be right for you or your team. Maybe you need something more opinionated - or less? Maybe you need a tool backed by a large organisation or with a large community? Maybe you just don't like to be productive and happy? Who knows!

Anyway, Here are some key differences between Kegstand and some of the other tools out there.

...(more to come)
