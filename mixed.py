import sys
import subprocess
import random
import json
import pprint
import bisect


NUM_ROUNDS = 50


# This represents the graph JSON file.
filename = sys.argv[1]
info = filename.split('.')
num_players = int(info[0])
num_seeds = int(info[1])
graph_id = int(info[2])

subprocess.call(["python", "deg_centrality.py", filename])
subprocess.call(["python", "deg_centrality2.py", filename])
subprocess.call(["python", "bridges.py", filename])

def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect.bisect(cum_weights, x)
    return values[i]


myfile = open("submit.txt", "w")
best_nodes_choice = {}

bridges_choice = {}
deg_centrality_choice = {}
deg_centrality2_choice = {}
for line in open("bridgeNodes.txt","r"):
    key, val = line.split(",")
    bridges_choice[key] = float(val)

for line in open("deg_centrality.txt","r"):
    key, val = line.split(",")
    deg_centrality_choice[key] = float(val)

for line in open("deg_centrality2.txt","r"):
    key, val = line.split(",")
    deg_centrality2_choice[key] = float(val)



tuplelist1 = [(v,k) for v,k in bridges_choice.iteritems()]
tuplelist2 = [(v,k) for v,k in deg_centrality_choice.iteritems()]
tuplelist3= [(v,k) for v,k in deg_centrality2_choice.iteritems()]




for i in range(NUM_ROUNDS):
    seeds = []
    while (len(seeds) < num_seeds):
        temp = random.choice([tuplelist1,tuplelist2,tuplelist3])
        seed = weighted_choice(temp)
        if seed in seeds:
            pass
        else:
            seeds.append(seed)
    for seed in seeds:
        myfile.write("%d\n" %(int(seed)))


