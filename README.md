<!-- markdownlint-disable first-line-h1 line-length no-inline-html -->
<p align="center">
  <a href="https://kegstand.dev/">
    <img src="https://kegstand.dev/assets/kegstand-logotype.png" width="540px" alt="Kegstand logo" />
  </a>
</p>

<h3 align="center">The Developer's Toolbelt For Accelerating <em>Mean Time To Party</em> on AWS</h3>
<p align="center">created by <a href="https://jensroland.com/">Jens Roland</a> and fueled by a non-zero amount of alcohol</p>
<p align="center"><a href="https://kegstand.dev/demo">Watch a 3-minute demo</a></p><!-- markdown-link-check-disable-line -->

<br />

## 🥂💃🕺 Welcome to the Party! 🥂💃🕺

Kegstand is a free and open-source framework for creating Python APIs and services. It allows you to rapidly build and deploy services on AWS. We all have better things to do than `print(json.dumps(event))` all day long, and Kegstand is here to help you get to the party &mdash; _and into Prod_ &mdash; a lot faster.

**It provides:**

- A CLI tool for creating and deploying your services.
- A decorator based API abstracting away the boilerplate of Lambda, API Gateway, Cognito, and more.
- The full power of CDK to define and deploy arbitrary AWS resources with your services.

Experience a streamlined cloud development process, enhanced productivity, and hit that "party" button sooner with Kegstand!

Learn more on the [Kegstand website](https://kegstand.dev/).

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation) (recommended)
- An [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
- The [CDK CLI configured on the local machine and initialized on the AWS account](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- AWS CLI [configured with credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [Copier](https://copier.readthedocs.io/en/stable/#installation) project scaffolding tool (recommended)
- [npx](https://docs.npmjs.com/cli/v9/commands/npx) for installing CLI tools (recommended)
- A well-poured [Belgian style brown ale](https://www.grimbergen.com/)

## Quick start

To create a service with Kegstand, you'll need a Python project with a few dependencies and a folder structure following the Kegstand convention.

You can create this in a few seconds, either with the Kegstand CLI or using [Copier](https://copier.readthedocs.io/en/stable/#installation).

```shell
# Using the Kegstand CLI
> pipx install kegstandcli
> keg new my-service

# Using Copier
> copier gh:JensRoland/kegstand-project-template my-service
```

Either method will create a new project folder called `my-service` containing:

```shell
my-service
├── .gitignore                        # Standard .gitignore file
├── pyproject.toml                    # Project configuration
└── src
    └── api
        └── resources
            └── hello
                └── any.py            # Logic for /hello/
```

Kegstand projects are minimal by design, so a fresh project folder contains just those 3 files. Well, apart from a few empty `__init__.py` gatecrashers, but we can safely ignore those.

To install the dependencies for the new project:

```shell
> cd my-service
> poetry install
```

Finally, to build and deploy the service to AWS:

```shell
# Either activate the virtual environment first:
> poetry shell
> keg deploy

# Or simply run:
> poetry run keg deploy
```

You should now be able to access the API endpoint at `https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello`.

## Documentation

For more information, see the [official Kegstand documentation](https://kegstand.dev/docs).<!-- markdown-link-check-disable-line -->

## Roadmap

Here are some notable changes, fixes and features that are planned for development:

### 0.3.0

- [ ] Website up on [kegstand.dev](https://kegstand.dev)
- [X] Rename repos: kegstand should have been kegstand-framework-python. And kegstand-cli repo should be kegstand
- [X] Use the Copier template from github, not /template
- [X] Refactor README - move docs under /docs
- [X] Lint code with [Black](https://black.readthedocs.io/en/stable/) etc.

## 0.4.0

- [ ] Custom domain names

### Pre-1.0.0

- [ ] Specify event triggers for Lambda functions: S3, SNS, SQS, DynamoDB, Cloudwatch CRON scheduled events, etc.
- [ ] Pagination helper
- [ ] [Record a screencast](https://asciinema.org/) for the README
- [ ] Autogenerated docs using [MkDocs](https://www.mkdocs.org/)
- [ ] GitHub Actions workflow for pushing docs to the website

### 1.0.0

- [ ] Intuitive and mostly automated API Versioning
- [ ] Simple way to define/override core API/Lambda properties such as CPU/MEM, Python runtime version, warm pool (!), and concurrency
- [ ] Deploy Lambda-only microservices with no API Gateway

### Future

- [ ] Configurable log level
- [ ] Add AWS tags in the Kegstand config and they will be applied to the generated resources
- [ ] Easily add [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [ ] Add support for APIs using [FastAPI](https://fastapi.tiangolo.com/) with [Mangum](https://mangum.io/) instead of the default Kegstand API framework, and just provide deployment helpers for the API Gateway and Lambda
- [ ] Improved output from deploy command; friendly post-deploy instructions for testing your API
- [ ] Version bumper with [bump2version](https://pypi.org/project/bump2version/)
- [ ] Include more goodies from [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.11.0/) - tracing, metrics, etc.
- [ ] Add support for APIs using pure [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.11.0/) instead of the default Kegstand API framework, and just provide deployment helpers for the API Gateway and Lambda
- [ ] Unit testing helpers (wrap moto and make it all a little more DRY and intuitive)
- [ ] Secure endpoints which require re-authentication (and/or MFA) so a refreshed token isn’t enough (to, say, delete your account or change your credit card info)
- [ ] Live Lambda development a la SST
- [ ] Build and deploy gRPC endpoints (or similar alternative)
- [ ] Build and deploy GraphQL endpoints
- [ ] Build and deploy stream processors?
- [ ] Option to teardown before deploying: `keg deploy --force-redeploy`
- [ ] Use env vars to populate values in kegstand.toml
- [ ] Merge Kegstand and Beth into one tool
- [ ] CDK Pipelines
- [ ] Support HTTP method-specific files (e.g. `get.py`, `post.py`, etc.)
- [ ] Upgrade Copier once the [template-deleting bugfix](https://github.com/copier-org/copier/pull/1037) is released
