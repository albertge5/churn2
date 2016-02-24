import sim
import sys
import numpy as np
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

keys1 = scores.keys()
keys2 = scores[keys1[0]].keys()
lookUp1 = {keys1[i]: i for i in range(len(keys1))}
lookUp2 = {keys2[i]: i for i in range(len(kyes2))}
scoreMatrix = np.zeros(len(keys1), len(keys2))
for key1 in keys1:
    for key2 in keys2:
        scoreMatrix[lookUp1[keys1]][lookUp2[keys2]] = scores[key1][key2]

np.savetxt('costMatrix.csv', scoreMatrix, delimiter=",")



            
