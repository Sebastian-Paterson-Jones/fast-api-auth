# pull official base image
FROM python:3.9-slim-buster

# set working directory
WORKDIR /usr/app

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY src .