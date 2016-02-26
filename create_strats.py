import json
import networkx as nx
import heapq
import sys
from tqdm import *
import os
import subprocess

filename = '2.5.2'
nodes = 10
if len(sys.argv) > 1:
    filename = sys.argv[1]
if len(sys.argv) > 2:
    nodes = int(sys.argv[2])
print filename
print nodes

# Doing bridge nodes.
subprocess.call(["python", "bridges.py", filename])
bridgeFile = open("bridgeNodes.txt", "r")
bridgeNodes = []
for line in bridgeFile:
    if line != "":
        bridgeNodes.append(int(line.rstrip()))



G = nx.Graph()
with open(filename) as json_file:
    data = json.load(json_file)
    for i in range(len(data)):
        G.add_node(i)
        for j in range(len(data[str(i)])):
            G.add_edge(i, int(data[str(i)][j]))

# Measuring using degrees.
bridgeDegrees = nx.degree(G, bridgeNodes)


bc = nx.betweenness_centrality(G)
cc = nx.closeness_centrality(G)
dc = nx.degree_centrality(G)
print "graph analysis completed"

# Going to also look at bridge nodes. I'm going to add some to all
# current nodes.
def gen_strats(res, nodes):
    topBridgeNodes = []
    for key in bridgeDegrees:
        degreeVal = bridgeDegrees[key]
        if len(topBridgeNodes) < nodes / 4:
            heapq.heappush(topBridgeNodes, (degreeVal, key))
        elif degreeVal > topBridgeNodes[0][0]:
            heapq.heappop(topBridgeNodes)
            heapq.heappush(topBridgeNodes, (degreeVal, key))

    print topBridgeNodes
    
    strats = {}
    for alpha in tqdm(range(0, 100 + res, res)):
        for beta in range(0, 100 + res - alpha, res):
            gamma = 100 - alpha - beta

            for pagerank in [True, False]:
                init_scores = []
                top = []
            
                #linear combination of BC, CC, DC
                for i in range(len(G.nodes())):
                    score = alpha / 0.07 * bc[i] + beta / 0.54 * cc[i] + gamma / 0.28 * dc[i]
                    init_scores.append(score)
            
                #pagerank like algo
                for i in range(len(G.nodes())):
 
                    new_score = init_scores[i]
                    if pagerank:
                        for nbr in G.neighbors(i):
                            new_score += init_scores[nbr] / G.degree(nbr)

                    if len(top) < nodes - nodes / 4:
                        heapq.heappush(top, (new_score, i))   
                    elif new_score > top[0][0]:
                        heapq.heappop(top)
                        heapq.heappush(top, (new_score, i))
   
                best_nodes = []
                for score, i in top:
                    best_nodes.append(i)

                for degree, j in topBridgeNodes:
                    best_nodes.append(j)

                key = 'lin comb with bridge: (' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + ',' + str(pagerank) + ')'
                strats[key] = best_nodes

    for alpha in tqdm(range(nodes - nodes / 4)):
        for beta in range((nodes - nodes / 4) - alpha):
            gamma = (nodes - nodes / 4) - alpha - beta
            for pagerank in [True, False]:
                tops = [[], [], []]
                for i in range(len(G.nodes())):
                    newB = bc[i]
                    newC = cc[i]
                    newD = dc[i]
                    if pagerank:
                        for nbr in G.neighbors(i):
                            newB += bc[nbr] / G.degree(nbr)
                            newC += cc[nbr] / G.degree(nbr)
                            newD += dc[nbr] / G.degree(nbr)
                    for top, new_score, thresh in zip(tops, [newB, newC, newD], [alpha, beta, gamma]):
                        if len(top) < thresh:
                            heapq.heappush(top, (new_score, i))
                        elif thresh > 0 and new_score > top[0][0]:
                            heapq.heappop(top)
                            heapq.heappush(top, (new_score, i))
                best_nodes = []
                for top in tops:
                    for score, i in top:
                        best_nodes.append(i)
                for degree, j in topBridgeNodes:
                    best_nodes.append(j)

            key = 'mixed with bridge: (' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + ',' + str(pagerank) + ')'
            strats[key] = best_nodes

    # Finding the best bridge nodes.
    return strats
                            
our_strats = gen_strats(5, nodes)
ta_strats = gen_strats(10, int(nodes * 1.2))

with open("output/" + filename[:-5] + "/p1.txt", "w") as outfile:
    json.dump(our_strats, outfile)
    
with open("output/" + filename[:-5] + "/p2.txt", "w") as outfile:
    json.dump(ta_strats, outfile)

os.system('cp ' + filename + ' output/' + filename[:-5] + '/' + filename)

