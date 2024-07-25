from neo4j import GraphDatabase

class Sloth:
    def __init__(self, uri: str = "bolt://localhost:7687", Auth: tuple = ("neo4j", "12345678")) -> None:
        self.uri = uri
        self.auth = Auth
        with GraphDatabase.driver(uri, auth=Auth) as driver:
            try:
                print("Checking connection with Neo4j...")
                driver.verify_connectivity()
                print("Connection with driver verified!")
            except Exception as e:
                print(e)
                raise e

    def read_node(self, query: str | dict, logical_operator: str = "AND") -> list:
        """
        Reads nodes from the Neo4j graph database.

        Params:
        query (str | dict): The query parameter can be either a string or a dictionary.
            - If the query is "*", it returns all nodes.
            - If the query is a dictionary, it returns nodes that match the specified properties. For example:
              query = {"name": "John", "age": 22}

        logical_operator (str): The logical operator to be used between multiple conditions in the query. Default is "AND". Possible values are "AND" and "OR".

        Returns:
        list: A list of dictionaries, each representing the properties of the retrieved nodes, including a generated node ID.
        """
        try:
            with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
                if query == "*":
                    with driver.session() as session:
                        records = session.run("MATCH (n) RETURN (n)")
                        res = []
                        for record in records:
                            node = record['n']
                            rec_properties = dict(node)
                            rec_properties.update({'id': int(node.element_id.split(":")[2])})
                            res.append(rec_properties)
                    return res
                else:
                    conditions = []
                    for key, value in query.items():
                        if isinstance(value, str):
                            conditions.append(f"n.{key}='{value}'")
                        else:
                            conditions.append(f"n.{key}={value}")
                    condition_str = f" {logical_operator} ".join(conditions)
                    
                    with driver.session() as session:
                        records = session.run(f"MATCH (n) WHERE {condition_str} RETURN (n)")
                        res = []
                        for record in records:
                            node = record['n']
                            rec_properties = dict(node)
                            rec_properties.update({'id': int(node.element_id.split(":")[2])})
                            res.append(rec_properties)
                    return res
        except Exception as e:
            raise e
