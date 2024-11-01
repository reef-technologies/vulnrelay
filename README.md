# vulnrelay

Run vulnerabilities scanner(s) and sync findings

## Development

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)

### Setup

Install the dependencies:

```bash
uv sync
```

Setup the pre-commit hooks:

```bash
uv run pre-commit install
```

### Testing

Run the test suite:

```bash
uv run pytest
```

Start the test watcher:

```bash
uv run ptw .
```
