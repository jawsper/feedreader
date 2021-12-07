FROM node:14 AS node-builder

WORKDIR /app

COPY feedreader_gui/package.json \
    feedreader_gui/yarn.lock \
    feedreader_gui/webpack.config.js \
    /app/
COPY feedreader_gui/assets /app/assets/

RUN yarn --frozen-lockfile && \
    ls /app && \
    yarn run build && \
    rm -r node_modules

# pull official base image
FROM python:3.9-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# Install build dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev zlib-dev jpeg-dev

# install dependencies
RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

# Remove build dependencies
RUN apk del build-deps

# copy entrypoint.sh
# COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . .

RUN addgroup \
    --system \
    feedreader \
    && adduser \
    --system \
    --home "$(pwd)" \
    --disabled-password \
    --no-create-home \
    --ingroup feedreader \
    feedreader

RUN chown -R feedreader .

USER feedreader

COPY --from=node-builder --chown=feedreader /app/static ./feedreader_gui/static/
COPY --from=node-builder --chown=feedreader /app/webpack-stats.json ./feedreader_gui/

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
