FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1

# required packages
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends default-libmysqlclient-dev
RUN apt-get install -y gcc git libc-dev python3-dev python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

## make a local directory
RUN mkdir /app

# set "app" as the working directory from which CMD, RUN, ADD references
WORKDIR /app

# now copy all the files in this directory to /app
ADD . /app

# pip install the local requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Listen to port 8000 at runtime
EXPOSE 8000
