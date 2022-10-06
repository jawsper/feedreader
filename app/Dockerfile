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
    && addgroup \
    --system \
    feedreader \
    && adduser \
    --system \
    --home "$(pwd)" \
    --disabled-password \
    --no-create-home \
    --ingroup feedreader \
    feedreader \
    && mkdir media static \
    && chown -R feedreader .

USER feedreader

# copy project
ENV PATH=/app/.venv/bin:$PATH
COPY --from=builder --chown=feedreader /app/.venv/ ./.venv/
COPY --chown=feedreader feedreader ./feedreader
COPY --chown=feedreader feedreader_api ./feedreader_api
COPY --chown=feedreader feedreader_gui ./feedreader_gui
COPY --chown=feedreader manage.py .
COPY --chown=feedreader entrypoint.sh .
COPY --from=node-builder --chown=feedreader /app/static ./feedreader_gui/static/
COPY --from=node-builder --chown=feedreader /app/webpack-stats.json ./feedreader_gui/

# ENTRYPOINT ["/app/entrypoint.sh"]
