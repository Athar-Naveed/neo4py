from setuptools import setup, find_packages

setup(
    name="neo4py",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "neo4j>=5.20"
    ],
)
