import unittest

import HetClass
from HetClass.models.HetGraph import HetGraph

class modelTester(unittest.TestCase):
    def test_0(self):
        G = HetGraph()
        G.read_database()
        assert True

    def test_get_m(self):
        G = HetGraph()
        G.read_database()
        assert G.get_m() == 3

    def test_get_n(self):
        G = HetGraph()
        G.read_database()
        assert G.get_n("type0") == 4 and G.get_n("type1")==6 and G.get_n("type2")==5

    def test_get_K(self):
        G = HetGraph()
        G.read_database()
        assert G.get_K() == 1

    def test_get_class(self):
        G = HetGraph()
        G.read_database()
        assert G.get_class("type0",0) == "INIT" and G.get_class("type0",1) is None

    def test_get_labels(self):
        G = HetGraph()
        G.read_database()
        assert len(G.get_labels()) == 1
    
if __name__ == "__main__":

    unittest.main()
