FROM python:3.8-buster

RUN mkdir -p /opt/project
WORKDIR /opt/project

COPY . /opt/project

RUN apt-get -qqy update && \
    apt-get install -qqy x11-apps

#Dont forget to run
# docker run --rm -ti -e DISPLAY -v $PWD:/opt/project -v /tmp/.X11-unix:/tmp/.X11-unix --user="$(id --user):$(id --group)" smpiano/calc:0.0.1 /bin/bash
