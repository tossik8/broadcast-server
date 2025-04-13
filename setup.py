from setuptools import setup, find_packages

name = "broadcast-server"

setup(
    name=name,
    version="0.1.0",
    author="Nikita Toropov",
    packages=find_packages(),
    python_requires=">= 3.12",
    entry_points={
        "console_scripts": [
            f"{name} = src.main:main"
        ]
    },
    url="https://github.com/tossik8/broadcast-server.git"
)
