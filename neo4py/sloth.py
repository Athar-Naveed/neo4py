from neo4j import GraphDatabase 
class Sloth():
    def __init__(self,uri,Auth):
        self.uri = uri
        self.auth = Auth

    def create_node(self, nodes):
        try:
            with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
                for node in nodes:
                    labels = ":".join([node["label"]] if isinstance(node["label"],str) else node["label"])
                    query = f"CREATE (:{labels} $props)"
                    try:
                        with driver.session() as session:
                            session.run(query,props=node)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
    # ===========================
    # ===========================
    # ===========================
    def read_node(self,query:str|dict):
        """
        we have to add 2 ways of reading nodes:
        1. All the nodes: '*'
        2. A Specific node
        """
        try:
            with GraphDatabase.driver(self.uri,auth=self.auth) as driver:
                if query == "*":
                    with driver.session() as session:
                        records = session.run("MATCH (n) RETURN (n)")
                        res = list()
                        for record in records:
                            node = record['n']
                            rec_properties = dict(node)
                            rec_properties.update({'id':int(node.element_id[-1])})
                            res.append(rec_properties)
                    return res
        except Exception as e:
            print(e)

