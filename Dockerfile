FROM python:3.12-alpine

RUN apk update && apk add --no-cache docker

COPY --from=ghcr.io/astral-sh/uv:0.4 /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
	--mount=type=bind,source=uv.lock,target=uv.lock \
	--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --frozen --no-dev

COPY src/ /app

COPY cron/entry /etc/crontabs/root

CMD ["crond", "-f", "-d", "8", "-c", "/etc/crontabs"]
