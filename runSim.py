import sim
import sys
import subprocess
import json
import os

# file represents the JSON file.

# The JSON is in the format:
# numPlayers.numSeeds.uniqueID.json
from tqdm import *
dir = 'output'
scores = {}
for dirName in os.listdir(dir):
    data = {}
    if dirName.startswith('.'):
        continue
    for fname in os.listdir(dir + '/' + dirName):
        if fname[-5:] == '.json':
            with open(dir + '/' + dirName + '/' + fname, 'r') as f:
                adj_list = json.load(f)
        else:
            with open(dir + '/' + dirName + '/' + fname, 'r') as f:
                print('loading %s into %s' %(fname, fname[:2]))
                data[fname[:2]] = json.load(f)

    iter = 0
    for key1, val1 in tqdm(data['p1'].iteritems()):


        for key2, val2 in data['p2'].iteritems():
            d = {'p1': [str(x) for x in val1], 
                 'p2': [str(x) for x in val2]}
            
            temp = scores.get(key1,{})
            temp[key2] = temp.get(key2, 0) + sim.run(adj_list, d)['p1']
            scores[key1] = temp

with open('costMatrix', 'w') as f:
    json.dump(scores, f)




            
