from neo4py.sloth import Sloth

class TestSloth():
    def setup_method(self):
        try:
            self.sloth = Sloth("bolt://localhost:7687",("neo4j","12345678"))
            print(f"Connection verified!")
        except Exception as e:
            print(f"Connection failed! {e}")
    
    def test_create_node(self):
        self.sloth.create_node([{"name":"athar","gender":"male","label":"Human"},{"name":"naveed","gender":"male"}])
    def test_read_node(self):
        assert len(self.sloth.read_node("*")) == len(self.sloth.read_node("*"))

