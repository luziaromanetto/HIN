import unittest

import HetClass
from HetClass.methods.GNetMine import GNetMine
from HetClass.models.HetGraph import HetGraph

class GNetMineTester(unittest.TestCase):
    def test_0(self):
        M = GNetMine()

    def test_run(self):
        G = HetGraph()
        G.read_database()

        M = GNetMine(graph = G)
        M.run()

if __name__ == "__main__":
    unittest.main()
