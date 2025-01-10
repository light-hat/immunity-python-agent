FROM python:3.12

WORKDIR /build

COPY . /build

RUN VERSION=$(cat VERSION) \
    && sed -i "s/0.0.0/$VERSION/" setup.py \
    && sed -i "s/0.0.0/$VERSION/" pyproject.toml

RUN python3 -m pip install --upgrade build

RUN python3 -m build --sdist --wheel

RUN pip install dist/*.tar.gz
