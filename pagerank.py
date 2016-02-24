import json
import sys
from pprint import pprint
import heapq
import csv
'''
This file is designed to do pagerank on the undirected graph.
We will use the algorithm that we used for mapreduce, we just won't 
be mapreducing anything.

This means that we will sum up the rankings of neighbors, divided by 
the degree.
'''

def pageRank(rounds):
    # This is the JSON file that will be parsed.
    JSONfile = sys.argv[1]

    # Recall that the JSON file is in the form:
    # num_players.num_seeds.uniqueID
    JSONinfo = JSONfile.split('.')
    numPlayers = int(JSONinfo[0])
    numSeeds = int(JSONinfo[1])
    uniqueID = int(JSONinfo[2])

    with open(JSONfile) as dataFile:
        JSONdata = json.load(dataFile)

    