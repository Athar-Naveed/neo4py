from neo4j import GraphDatabase 
class Sloth():
    def __init__(self,uri,Auth):
        self.uri = uri
        self.auth = Auth

    def create_node(self, nodes)->dict:
        """
        It creates nodes in the graph, you have to pass the nodes data as a list of dictionaries.
        
        Params:
        nodes (list of dict): You can pass data to it like this:
        nodes = [{"name":"John","age":30,"gender":"male"},{"name":"Jane","age":25,"label":["Person","Human"]}]

        Return:
        dict: It will return the data in the form of dictionary, which you can access.

        """
        returned_data = []
        try:
            with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
                for node in nodes:
                    if "label" in node.keys():
                        labels = ":".join([node["label"]] if isinstance(node["label"], str) else node["label"])
                        query = f"CREATE (n:{labels} $props) RETURN (n)"
                    else:
                        query = f"CREATE (n $props) RETURN (n)"
                    
                    with driver.session() as session:
                        result = session.run(query, props=node)
                        for record in result:
                            data = record["n"]._properties
                            data.update({'id':record['n'].element_id.split(":")[2]})
                            returned_data.append(data)
        except Exception as e:
            raise e
        
        return returned_data
    # ===========================
    # ===========================
    # ===========================
    def read_node(self,query:str|dict):
        """
        It returns all nodes as a list of dictionary

        Params:
        query (str|dict): For string: 
        You can pass data like this, sloth.read_node("*"), it'll return the whole data

        For dict:
        You can pass data like this, sloth.read_node({"name":"John"}), it'll return the data where name is John

        Return:
        list: It will return the data in the form of list of dictionaries, which you can iterate over to access your desired data.
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
                            rec_properties.update({'id':int(node.element_id.split(":")[2])})
                            res.append(rec_properties)
                    return res
                else:
                    keys,values = '',''
                    for key,value in query.items():
                        keys = key
                        values = value
                    with driver.session() as session:
                        records = session.run("MATCH (n) WHERE n.{}='{}' RETURN (n)".format(keys,values))
                        res = list()
                        for record in records:
                            node = record['n']
                            rec_properties = dict(node)
                            rec_properties.update({'id':int(node.element_id.split(":")[2])})
                            res.append(rec_properties)
                    return res
        except Exception as e:
            raise e
