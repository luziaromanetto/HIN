import csv
import random
import sys
import shutil
import os

if __name__ == "__main__":
    dirpath = sys.argv[1]
    print dirpath

    files = [ f for f in os.listdir(dirpath) if f.endswith(".bak") ]
    for f in files:
        os.remove(os.path.join(dirpath, f))

    m = 3
    n = [4, 6, 5]

    for typei in range(m):
        with open(dirpath+"type%d.tsv"%(typei,), "wb") as f:
            writer = csv.writer(f, delimiter="\t")
            for node in range(n[typei]):
                if typei == 0 and node == 0 :
                    writer.writerow( [str(node), "node%d_type%d"%(node, typei), "INIT" ])
                else:
                    writer.writerow( [str(node), "node%d_type%d"%(node, typei), "NULL" ])

    prob1 = 0.5
    prob2 = 0.5
    for typei in range(m):
        for typej in range(typei, m):
            prob = random.random()
            if prob > prob1 :
                with open(dirpath+"type%d_type%d.tsv"%(typei,typej), "wb") as f:
                    writer = csv.writer(f, delimiter="\t")
                    for nodei in range(n[typei]):
                        for nodej in range(nodei, n[typej]):
                            prob = random.random()
                            if prob > prob2:
                                writer.writerow([ nodei, nodej, "edge_node%dtype%d_node%dtype%d"%(typei,nodei,typej,nodej) ])
