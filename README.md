# UPS017

## Local setup

Project uses Python 3.10.0 version

To run application locally, create and activate poetry environment:

```bash
poetry install

poetry shell


```

To run tests, execute:

```bash
pytest
```

To run static code analysis for all code repo, execute:

```bash
black .
mypy .
pylint src tests
```

To create image of db:
```bash
docker compose up
```