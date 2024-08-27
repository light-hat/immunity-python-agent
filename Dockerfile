FROM python:3.12

WORKDIR /build

COPY . /build

RUN python3 -m pip install --upgrade build

RUN python3 -m build

RUN ls -la dist | grep agent && echo "PACKAGE FOUND!"

RUN pip install dist/*.tar.gz

RUN pip freeze | grep immunity-python-agent && echo "AGENT FOUND!"
