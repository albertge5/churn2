import json
import sys
from pprint import pprint
import heapq

'''
This file is designed to find the bridge nodes on the undirected graph.
We will use Tarjan's linear-time algorithm to find the bridges of 
a graph.

I assume that the higher the degree of a bridge vertex, the more we want
that vertex to be a part of our initial seeding.
'''
def findMinSpanTree(adjacencyList):
    
def findBridges(adjacencyList):

# This basically parses the stuff and then invokes the bridge.
def run(rounds = 50):
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

    # Storing the top nodes for optimal choices.
    topNodes = []

    # Storing the adjacency matrix of the entire thing.
    adjacencyList = {}

    # Populating this beautiful dictionary.
    for key, val in JSONdata.iteritems():
        adjacencyList[key] = val

if __name__ == '__main__':

    # If the number of arguments isn't correct, we print a usage thing.
    if len(sys.argv) != 3:
        print "Usage: python", sys.argv[0], "GRAPH.json WEIGHTS.csv [ITERATIONS]\n" \
              "Example: python", sys.argv[0], "2.5.1.json weights.csv"
        sys.exit()

    if len(sys.argv) == 4:
        rounds = int(sys.argv[3])
        run(rounds = rounds)
    else:
        run()