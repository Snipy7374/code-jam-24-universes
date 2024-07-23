FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PATH=/app/.venv/bin:$PATH

RUN set -ex \
    && addgroup --gid 50000 python \
    && adduser --shell /bin/false --disabled-password --uid 50000 --gid 50000 --home /python python \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

USER python
WORKDIR /app

FROM base AS build

# Install project dependencies
RUN python -m pip install --no-cache --disable-pip-version-check --user poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true

COPY pyproject.toml poetry.lock ./
RUN /python/.local/bin/poetry install --no-root --no-dev --sync --no-ansi --no-interaction

FROM base AS runtime
COPY --from=build /app/.venv /app/.venv

# Copy the source code in last to optimize rebuilding the image
COPY --chown=python:python . .

ENTRYPOINT ["python", "-m", "src"]
