import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neo4py",
    version="1.1.0",
    author="Athar Naveed",
    author_email="asphaltlegends24@gmail.com",
    description="Neo4py is a better alternative to py2neo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["neo4j","alternative","neo4py","py2neo","graph database"],
    url="https://github.com/Athar-Naveed/neo4py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "neo4j"
    ],
)
