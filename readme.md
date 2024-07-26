## Neo4py
A proper documentation to __neo4py__ is available [here](https://neo4pydocs.vercel.app/).
## Introduction
Neo4py is an alternative to __py2neo__. I am trying my best to make it a perfect and better clone of the py2neo package.

### How to run a query in neo4py
As it is a clone of py2neo so, I have added the similar functions like of py2neo so, that the users won't have the problem in migrating from py2neo to neo4py. 

These are the steps you can use to execute a query in neo4py:

<br>

1. First install `neo4j` using either __pip__ or __uv__.

```
pip install neo4j

# or you can use uv for this

uv pip install neo4j
```

<br>

2. Import the `Graph` class from the `neo4py`.

<br>

```
from neo4py.neo4py import Graph
```

<br>


3. Create a `graph` object and pass your __URI__, and __connection details__ to the `Graph` constructor.

<br>

```
graph = Graph("connection_uri",("user","db_password"))
```
<br>

```
# Example code
graph = Graph("bolt://localhost:7687",("neo4j","12345678"))
```

<br>

You can find your connection uri and user details, when you'll start your database and open __neo4j browser__. 
__Password__ is the password that you have set while creating the database.

<br>


4. Now make a __python dictionary__, pass the data to it, and run and write the query by using built-in __run method__.

<br>

```
data = {
    "name" : "John Doe",
    "age": 21
}
node = graph.run("CREATE (p:Person {name:$name,age:$age})", **data)

```


### Final Words
For any issues, please open an issue.
I am open for suggesstions, contributions, and collaborations.😊

<br>

Special Thanks to [Aaron Moffatt](https://pypi.org/user/AaronM/) for letting me acquire the name, __"neo4py"__