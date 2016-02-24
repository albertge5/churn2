import json
import networkx as nx
import heapq
import sys

filename = '2.5.2'
nodes = 5
if len(sys.argv) > 2:
    filename = sys.argv[1]
    nodes = int(sys.argv[2])
print filename
print nodes

G = nx.Graph()
with open(filename) as json_file:
    data = json.load(json_file)
    for i in range(len(data)):
        G.add_node(i)
        for j in range(len(data[str(i)])):
            G.add_edge(i, int(data[str(i)][j]))

bc = nx.betweenness_centrality(G)
cc = nx.closeness_centrality(G)
dc = nx.degree_centrality(G)

def gen_strats(res, nodes):
    strats = {}
    for alpha in range(0, 100 + res, res):
        for beta in range(0, 100 + res - alpha, res):
            gamma = 100 - alpha - beta
            init_scores = []
            top = []
            
            #linear combination of BC, CC, DC
            for i in range(len(G.nodes())):
                score = alpha / 0.07 * bc[i] + beta / 0.54 * cc[i] + gamma / 0.28 * dc[i]
                init_scores.append(score)
            
            #pagerank like algo
            for i in range(len(G.nodes())):
                new_score = init_scores[i]
                for nbr in G.neighbors(i):
                    new_score += init_scores[nbr] / G.degree(nbr)

                if len(top) < nodes:
                    heapq.heappush(top, (new_score, i))   
                elif new_score > top[0][0]:
                    heapq.heappop(top)
                    heapq.heappush(top, (new_score, i))
   
            best_nodes = []
            for score, i in top:
                best_nodes.append(i)
            key = '(' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + ')'
            strats[key] = best_nodes
    return strats
                            
our_strats = gen_strats(5, nodes)
ta_strats = gen_strats(10, int(nodes * 1.2))

with open("p1.txt", "w") as outfile:
    json.dump(our_strats, outfile)
    
with open("p2.txt", "w") as outfile:
    json.dump(ta_strats, outfile)

