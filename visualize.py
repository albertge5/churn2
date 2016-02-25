import json
from networkx.readwrite import json_graph
import networkx as nx
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
G = nx.Graph()
with open(filename) as json_file:
    data = json.load(json_file)
    for key in data.keys():
        G.add_node(int(key))
        for val in data[key]:
            G.add_edge(int(key), int(val))
dic = {}
print G.size()
for i in range(len(G.nodes())):
    dic[i] = i
for i in range(1):
    plt.figure()
    plt.title('spring')
    nx.draw_spring(G, node_size=0,width=.2, labels=dic, font_size=8, font_color='red')


plt.show()

