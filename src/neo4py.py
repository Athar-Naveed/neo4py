from neo4j import GraphDatabase

class Graph:
    """Graph

    Constructor:
        The constructor of the Graph class takes 2 parameters  - uri and Auth.

        Params:
        uri (str): A string representing a URI to connect to Neo4j database, e.g., bolt://localhost:7687
        Auth (tuple): A tuple containing username and password for authentication against Neo4j Database.

    Run method:
        This is the main method that should be called after creating an instance of this class. It runs a Cypher query on the connected graph database
        to create or read a data from the node in Neo4j.

        Params:
        query (str): It takes a cypher query.
        **kwargs (dict): It takes the data in the dictionary format.

        Return:
        It returns the summary of the  result obtained by executing the query on the database.
    """
    def __init__(self,uri,Auth):
        self.uri = uri
        self.auth= Auth
        with GraphDatabase.driver(uri,auth=Auth) as driver:
            try:
                print("Checking connection with Neo4j...")
                driver.verify_connectivity()
                print("Connection with driver verified!")
            except Exception as e:
                print(e)
                print("\nCheck if your Neo4j is up and running or try restarting the Neo4j instance.")

    def run(self,query:str,**kwargs:dict)->list:
        """run method

        Params:
            query (str): It'll take user written cypher query, and pass it to execute_query method.
            **kwargs (dict): It can receive any number of keyword arguments which will be passed into the cypher query in execute_query method using dict.

        Returns:
            resp (list of dict): It'll return the data in the form of list of dictionaries, which you can iterate over to access your desired data.
            summary (default): By default, the summary of the executed query is returned.
        
        Example code:
            graph = Graph("connection_string",("username","password")) \n
            data = { \n
                "name":"Athar Naveed", \n
                "age":25 \n
            }
            query = "CREATE (p:Person {name:$name,age:$age}) return p" \n
            graph.run(query,**data) \n
        """
        with GraphDatabase.driver(self.uri,auth=self.auth) as driver:
            try:
                # ----------------------------
                # fetching data from database
                # ----------------------------
                records,summary,keys = driver.execute_query(query,**kwargs,database_=self.auth[0])
                # ----------------------------
                # checking for return statement
                # ----------------------------
                if "return" in query:
                    data_to_fetch = query.split("return")[1].strip().split(",")
                    resp:list = []
                    if data_to_fetch[0] == "(n)" or data_to_fetch[0] == "n":
                # ----------------------------
                # adding all the fetched nodes in to a list and making it a list of dictionaries
                # ----------------------------
                        for record in records:
                            rec = record.data()["n"]
                            rec.update({'id':record[0].element_id[-1]})
                            rec.update({'labels':list(record[0].labels)})
                            resp.append(rec)
                        return resp
                    else:
                # ----------------------------
                # if user has asked for a specific data like, n.name or n.age
                # ----------------------------
                        for record in records:
                            for prop in data_to_fetch:
                                resp.append(record.data()[prop])
                        return resp
                # ----------------------------
                # if no return statement, then return summary of the query executed.
                # ----------------------------
                return summary
            except Exception as e:
                print(e)
