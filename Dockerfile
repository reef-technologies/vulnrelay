FROM python:3.12-alpine

RUN apk update && apk add --no-cache docker

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync

COPY src/ /app

COPY cron/entry /etc/crontabs/root

CMD ["crond", "-f", "-d", "8", "-c", "/etc/crontabs"]
