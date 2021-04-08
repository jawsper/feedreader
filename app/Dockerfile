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

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
