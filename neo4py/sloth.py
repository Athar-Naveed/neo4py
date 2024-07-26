# ----------------------------
# Imports
# ----------------------------
from neo4j import GraphDatabase

# ----------------------------
# Sloth code
# ----------------------------
class Sloth:
    """
    Sloth class to interact with a Neo4j database.

    Constructor:
        The constructor of the Sloth class initializes the connection to the Neo4j database.

        Params:
        uri (str): A string representing a URI to connect to Neo4j database, e.g., bolt://localhost:7687. Default is "bolt://localhost:7687".
        Auth (tuple): A tuple containing username and password for authentication against Neo4j Database. Default is ("neo4j", "12345678").

    Methods:
        create_node: Creates nodes in the graph database.
        read_node: Reads nodes from the graph database.
    """

    # ----------------------------
    # Sloth constructor
    # ----------------------------
    def __init__(self, uri: str = "bolt://localhost:7687", Auth: tuple = ("neo4j", "12345678")) -> None:
        """
        Initializes the Sloth class and verifies the connection to the Neo4j database.

        Params:
        uri (str): A string representing a URI to connect to Neo4j database. Default is "bolt://localhost:7687".
        Auth (tuple): A tuple containing username and password for authentication against Neo4j Database. Default is ("neo4j", "12345678").
        """
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

    # ----------------------------
    # create node method
    # ----------------------------
    def create_node(self, nodes: list) -> list:
        """
        Creates nodes in the Neo4j graph database.

        Params:
        nodes (list of dict): A list of dictionaries containing node properties. For example:
            nodes = [{"name": "John", "age": 30, "gender": "male"},
                     {"name": "Jane", "age": 25, "label": ["Person", "Human"]}]

        Returns:
        list: A list of dictionaries, each representing the properties of the created nodes, including a generated node ID.
        """
        returned_data = []
        try:
            with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
                for node in nodes:
                    
                    # if a label is specified for a node or nodes
                    if "label" in node.keys():
                        labels = ":".join([node["label"]] if isinstance(node["label"], str) else node["label"])
                        query = f"CREATE (n:{labels} $props) RETURN (n)"

                    
                    else:
                        query = f"CREATE (n $props) RETURN (n)"
                    
                    with driver.session() as session:
                        result = session.run(query, props=node)
                        for record in result:
                            data = dict(record["n"])
                            data.update({'id': int(record['n'].element_id.split(":")[2])})
                            returned_data.append(data)
        except Exception as e:
            raise e
        
        # returning the created nodes in the form of list of dict
        return returned_data

    # ----------------------------
    # read node method
    # ----------------------------
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
                # in case of an asterik, all the nodes will be returned
                if query == "*":
                    with driver.session() as session:
                        records = session.run("MATCH (n) RETURN (n)")
                        res = []
                        for record in records:
                            node = record['n']
                            rec_properties = dict(node)
                            rec_properties.update({'id': int(node.element_id.split(":")[2])})
                            res.append(rec_properties)
                    # if a data is found it'll be returned else -1 will be returned with the message of data not found
                    if res:
                        return res
                    else:
                        return {"message":"No Data Found","status":-1}
                
                # if the user has queried a dict with the multiple number of keys, and operators this condition will handle that case
                else:
                    conditions = []
                    for key, value in query.items():
                        # if the value is a string, it'll be enclosed in single quotes else it'll be directly used in the query
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
                    
                    # if a data is found it'll be returned else -1 will be returned with the message of data not found
                    if res:
                        return res
                    else:
                        return {"message":"No Data Found","status":-1}
        
        except Exception as e:
            raise e

