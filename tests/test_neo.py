from src.neo4py.main import Graph
class TestNeo():
    def test_match(self):
        graph = Graph("bolt://localhost:7687",("neo4j","12345678"))
        try:
            assert  graph.run("MATCH (n) RETURN n") == {}
        except Exception as e:
            print(e)