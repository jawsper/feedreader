FROM node:16 AS node-builder

WORKDIR /app

COPY feedreader_gui/package.json \
    feedreader_gui/yarn.lock \
    feedreader_gui/webpack.config.js \
    feedreader_gui/tsconfig.json \
    /app/
COPY feedreader_gui/assets /app/assets/

RUN yarn --frozen-lockfile && \
    yarn run build && \
    rm -r node_modules

######################################

# pull official base image
FROM python:3.10-slim as builder

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIPENV_VENV_IN_PROJECT=1

# set work directory
WORKDIR /app

# Install build dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install --no-install-recommends -y python3-dev libpq-dev gcc

# install dependencies
RUN pip install pipenv==2022.5.2
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv sync

######################################

FROM python:3.10-slim as runtime

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install --no-install-recommends -y libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system feedreader \
    && adduser \
    --system \
    --home "$(pwd)" \
    --disabled-password \
    --no-create-home \
    --ingroup feedreader \
    feedreader \
    && mkdir media static \
    && chown feedreader media static

USER feedreader

# copy project
ENV PATH=/app/.venv/bin:$PATH
USER nobody
COPY --from=builder /app/.venv/ ./.venv/
COPY feedreader ./feedreader
COPY feedreader_api ./feedreader_api
COPY feedreader_gui ./feedreader_gui
COPY manage.py .
COPY entrypoint.sh .
COPY --from=node-builder /app/static ./feedreader_gui/static/
COPY --from=node-builder /app/webpack-stats.json ./feedreader_gui/

# ENTRYPOINT ["/app/entrypoint.sh"]
