# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build

# Опционально: ускорим и сделаем сборку чище
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN apt update -y && apt install -y gcc make cmake

RUN pip install --user --upgrade pip setuptools

RUN pip install --user . -v

RUN pip show dongtai_agent_python

