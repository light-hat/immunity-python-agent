import os

from setuptools import setup


def readme():
    with open("Readme.md", "r") as f:
        return f.read()


setup(
    name="immunity_agent_python",
)
