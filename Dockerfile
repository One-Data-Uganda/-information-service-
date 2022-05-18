# syntax = docker/dockerfile:experimental
FROM python:3.8-slim

LABEL com.centurylinklabs.watchtower.enable="true"

ADD requirements.txt /tmp/

RUN --mount=type=cache,target=/root/.cache/pip pip3.8 install -r /tmp/requirements.txt

USER nobody

COPY --chown=nobody . /project

WORKDIR /project

ENTRYPOINT [ "/project/entry-point.sh" ]
