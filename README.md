# vulnrelay

Run vulnerabilities scanner(s) and sync findings

## Development

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)

### Setup

```bash
./setup-dev.sh
```

### Usage

```bash
uv run python main.py
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
