# pull official base Docker image containing Python envrn
FROM python:3.11.2-slim-buster

# set working directory inside container
WORKDIR /usr/src/app

# set environment variables
#Prevents Python from writing .pyc files to disc.
#Ensures Python output is sent straight to terminal without being buffered.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean


# copy(from local to container)and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

