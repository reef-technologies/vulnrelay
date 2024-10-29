FROM python:3.12-alpine

RUN apk update && apk add --no-cache docker

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync

COPY src/ /app

CMD ["uv", "run", "python", "main.py"]
