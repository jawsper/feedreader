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

FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

######################################

FROM base as poetry

RUN python -m pip install poetry==1.6.1
COPY pyproject.toml poetry.lock ./
RUN poetry export -o requirements.txt

######################################

FROM base as builder

COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
RUN python -m venv .venv && \
    .venv/bin/pip install -U pip && \
    .venv/bin/pip install -r /tmp/requirements.txt

######################################

FROM base as runtime

RUN addgroup --system feedreader \
    && adduser \
    --system \
    --home "$(pwd)" \
    --disabled-password \
    --no-create-home \
    --ingroup feedreader \
    feedreader \
    && mkdir media static \
    && chown feedreader media static

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

USER feedreader

# ENTRYPOINT ["/app/entrypoint.sh"]
