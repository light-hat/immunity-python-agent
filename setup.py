from setuptools import find_packages, setup


def readme():
    with open("Readme.md", "r") as f:
        return f.read()


setup(
    name="immunity-python-agent",
    version="0.0.0",
    author="l1ghth4t",
    author_email="pirogov30002@gmail.com",
    description="Python-агент Immunity IAST для интерактивного сканирования веб-приложений.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    # url='your_url',
    packages=find_packages(),
    # install_requires=['requests>=2.25.1'],
    classifiers=[  # https://gist.github.com/nazrulworld/3800c84e28dc464b2b30cec8bc1287fc
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="iast security scanner ",
    project_urls={"GitVerse": "https://gitverse.ru/l1ghth4t/immunity-python-agent"},
    python_requires=">=3.9",
)
