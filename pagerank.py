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

# This invokes page rank.
def pageRank(topNodes, adjacencyList, weights, numSeeds):
    # Right now, we don't want to change the current weights vector.
    # So, we make two copies to use.

    # newWeights will be used to keep track of the old weights.
    newWeights = weights[:]

    # updatedWeights will be used to keep track of the updated weights.
    updatedWeights = newWeights[:]

    # Iterating through each key in the dictionary.
    # Recall that weights[key] refers to that key's current weight.
    for key in adjacencyList:
        neighbors = adjacencyList[key]

        # In case there are no neighbors, we don't update any of the
        # weights for that key.
        if neighbors[0] == "":
            continue

        # Otherwise, we look at the contributions.
        else:
            currNodeIdx = int(key)
            currNodeRank = newWeights[currNodeIdx]
            for neighbor in neighbors:
                neighborDegree = len(adjacencyList[neighbor])
                neighborIdx = int(neighbor)
                neighborRank = newWeights[neighborIdx]

                currNodeRank += neighborRank / float(neighborDegree)

            updatedWeights[currNodeIdx] = currNodeRank

        # Ensuring that we don't keep changing things over and over.
        newWeights = updatedWeights[:]
        updatedWeights = newWeights[:]

    # Finally, setting the value of the weights.
    # You could also do weights = updatedWeights I think, but
    # I'm doing this to play it safe.

    # We can also set the top nodes this way too.
    # Note: "i" denotes the node we are on, since the 
    #       index of the weight vector corresponds to the node Id.
    for i in range(len(weights)):
        weights[i] = updatedWeights[i]

        # Finding top nodes.

        # Condition if the topNodes isn't fully populated.
        if len(topNodes) < numSeeds:
            heapq.heappush(topNodes, i)

        # Condition if we find a node with rank larger than the
        # current minimum.
        elif updatedWeights[i] > topNodes[0]:
            heapq.heappop(topNodes)
            heapq.heappush(topNodes, i)

    # Now, sorting.
    top.sort(reverse = True)



# This basically just parses the stuff, and then invokes PageRank
def run(rounds = 2):
    # This is the JSON file that will be parsed.
    JSONfile = sys.argv[1]

    # Grabbing the weight file.
    weightFile = sys.argv[2]

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

    # Storing the weights of the nodes in this line.
    weights = []

    with open(weightFile, 'rb') as csvFile:
        weightReader = csv.reader(csvFile, delimiter=',', quotechar='"')

        # This weight file will only be one line.
        for row in weightReader:
            for weight in row:
                weights.append(float(weight))

    # Populating this beautiful dictionary.
    for key, val in JSONdata.iteritems():
        adjacencyList[key] = val

    # After this function, topNodes should be populated, as well as weights.
    # topNodes should be an array of ints
    # weights should be an array of floats.
    pageRank(topNodes, adjacencyList, weights, numSeeds)

    outFile = open("output.txt", "w")

    for i in range(rounds):
        for node in topNodes:
            outFile.write("%d\n" % node)


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


