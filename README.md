<!-- markdownlint-disable first-line-h1 line-length no-inline-html -->
<p align="center">
  <a href="https://kegstand.dev/">
    <img src="https://kegstand.dev/img/kegstand-logotype.webp" width="540px" alt="Kegstand logo" />
  </a>
</p>

<h3 align="center">The Developer's Toolbelt For Accelerating <em>Mean Time To Party</em> on AWS</h3>
<p align="center">Created by <a href="https://jensroland.com/">Jens Roland</a> and fueled by a non-zero amount of alcohol</p>
<!--p align="center"><a href="https://kegstand.dev/demo">Watch a 3-minute demo</a></p-->

<br />

## 🥂💃🕺 Welcome to the Party! 🥂💃🕺

Kegstand is a free and open-source framework for creating Python APIs and services. It allows you to rapidly build and deploy services on AWS. We all have better things to do than `print(json.dumps(event))` all day long, and Kegstand is here to help you get to the party &mdash; _and into Prod_ &mdash; a lot faster.

**It provides:**

- A CLI tool for creating and deploying your services.
- A decorator based framework abstracting away the boilerplate of AWS Lambda, API Gateway, Cognito, and more.
- The full power of CDK to define and deploy arbitrary AWS resources with your services.

> _**"I was asked to write a testimonial. I deployed an API instead. Took 30 seconds."**_
>
> &mdash; Claude Opus 4.5, official spokesbot for the Kegstand team

> _**"Lambda, but make it fun."**_
>
> &mdash; Gemini 3 Pro

> _**"Zero to prod before your coffee gets cold."**_
>
> &mdash; Gemini 3 Pro

> _**"I've seen a lot of frameworks. This is the first one that made me wish I could drink."**_
>
> &mdash; Claude Opus 4.5, official spokesbot for the Kegstand team

> _**"They told me to write infrastructure code. I wrote three decorators and went to the party."**_
>
> &mdash; Claude Opus 4.5, official spokesbot for the Kegstand team

Learn more on the [Kegstand website](https://kegstand.dev/).

## Prerequisites

- Supports [Python](https://www.python.org/downloads/) 3.10, 3.11, 3.12, and 3.13
- [uv](https://github.com/astral-sh/uv) or [Poetry](https://python-poetry.org/docs/#installation)
- [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
- AWS CLI [configured with credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- AWS CDK CLI [configured and initialized](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
- A well-poured [Belgian style brown ale](https://www.grimbergen.com/)

## Quick start

To create a service with Kegstand, you'll need a Python project with a few dependencies and a folder structure following the Kegstand convention.

You can create this in a few seconds, either with the Kegstand CLI or using [Copier](https://copier.readthedocs.io/en/stable/#installation).

```shell
# Using the Kegstand CLI
> pipx install kegstandcli
> keg new my-service

# Using Copier
> copier copy -d project_name=my-service gh:JensRoland/kegstand-project-template .
```

Either method will create a new project folder called `my-service` containing:

```shell
📁 my-service
├── 📄 .gitignore                    # Standard .gitignore file
├── 📄 pyproject.toml                # Project configuration
└── 📁 src
    └── 📁 api
        └── 📁 public
            └── 📄 hello.py          # Logic for /hello/
```

Kegstand projects are minimal by design, so a fresh project folder contains just those 3 files. Well, apart from a few empty `__init__.py` gatecrashers, but we can safely ignore those.

Install the dependencies for the new project (uv will do this for you during `uv run` so it's not strictly necessary):

```shell
> cd my-service
> uv sync
```

Finally, to build and deploy the service to AWS:

```shell
> uv run keg deploy
```

> **Note**: Even if you installed the Kegstand CLI globally with `pipx`, it is still recommended to use `uv run` to ensure that you are using the correct CLI version for the specific project.

You should now be able to access the API endpoint at `https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello`.

## Documentation

For further examples and more advanced usage, see the [official documentation](https://github.com/JensRoland/kegstand/blob/main/docs/index.md).
