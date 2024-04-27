from neo4j import GraphDatabase
from neo4py import Graph

class Sloth(Graph):
    def __init__(self):
        graph = Graph("bolt://localhost:7687", ("neo4j", "12345678"))
        self.uri = graph.uri
        self.auth = graph.auth

    def create_node(self, nodes):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            for node in nodes:
                labels = ":".join([node["label"]] if isinstance(node["label"],str) else node["label"])
                query = f"CREATE (:{labels} $props)"
                with driver.session() as session:
                    session.run(query,props=node)

sloth = Sloth()
sloth.create_node([{"name": "Athar", "age": 22,"label":"Human"},{"name": "Naveed", "age": 52,"label":["Person","Human"]}])
