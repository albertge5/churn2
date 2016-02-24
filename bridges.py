import json
import sys
from pprint import pprint
import heapq
import Queue

'''
This file is designed to find the bridge nodes on the undirected graph.
We will use Tarjan's linear-time algorithm to find the bridges of 
a graph.

I assume that the higher the degree of a bridge vertex, the more we want
that vertex to be a part of our initial seeding.
'''

# From just a list of edges, we will create the appropriate adjacencyList.
# Note: This graph is undirected, and we do not care about 0 degree nodes.
def createAdjList(edges):
    adjList = {}

    # Recall, edges are in tuple form. Each node is still in string form.
    for edge in edges:
        srcNode = edge[0]
        destNode = edge[1]

        # Since this is undirected, we ensure that the adjacency list 
        # goes both ways.
        if srcNode in adjList:
            adjList[srcNode].append(destNode)

        else:
            adjList[srcNode] = [destNode]

        if destNode in adjList:
            adjList[destNode].append(srcNode)

        else:
            adjList[destNode] = [srcNode]

    return adjList



# Like the name suggests, this simply just finds the minimum spanning tree
# of the graph.
def findMinSpanTrees(adjacencyList):
    # Since we don't really have any weights associated with each of
    # the edges, this algorithm is basically BFS. 
    # We take the first node in the adjacency list to be our start.

    # Edges will contain tuples, representing edges
    edges = []

    # Vertices will contain just string values of the node.
    vertices = []

    # In case the graph is disconnected, we will find several trees.
    treesAdjList = []
    treeEdges = []

    # We want the total number of vertices.
    numVertices = len(adjacencyList.keys())

    # Queue for BFS
    vertexQueue = Queue.Queue()

    # Start Index in case for disconnected nodes.
    startIdx = 0

    # We just operating on the first node.
    startNode = adjacencyList.keys()[startIdx]
    neighbors = adjacencyList[startNode]
    vertices.append(startNode)

    # We go until we find the first vertex with neighbors
    # That is, we go until we find our first connected component.
    while neighbors[0] == "" and startIdx < numVertices - 1:
        startIdx += 1
        startNode = adjacencyList.keys()[startIdx]
        neighbors = adjacencyList[startNode]
        vertices.append(startNode)

    # Once we hit a connected component, we start populating DAT QUEUE.
    for neighbor in neighbors:
        edge = (startNode, neighbor)
        vertexQueue.put(edge)

        vertices.append(neighbor)
        edges.append(edge)

    while len(vertices) == numVertices:
        # Two cases here:
        # 1: The queue is now empty (we exhausted this component)
        #       We first make an adjacency matrix for this.
        #       In this case, we keep incrementing startIdx until
        #       we encounter an unvisited connected component.
        #
        # 2: The queue is not empty
        #       In this case, we just keep going through that component.

        if vertexQueue.empty():
            # First, adding the new edges and the adjacency matrix into
            # the appropriate lists.
            treeEdges.append(edges)
            adjList = createAdjList(edges)
            treesAdjList.append(adjList)

            # Next, resetting the edge vector.
            edges = []

            # Now, we find the next connected component.
            if startIdx < numVertices - 1:
                startIdx += 1
                startNode = adjacencyList.keys()[startIdx]
                neighbors = adjacencyList[startNode]

                if startNode not in vertices:
                    vertices.append(startNode)  

            # We go until we find a vertex with neighbors
            # That is, we go until we find our connected component.
            while (neighbors[0] == "" or startNode in vertices) and \
                  startIdx < numVertices - 1:
                startIdx += 1
                startNode = adjacencyList.keys()[startIdx]
                neighbors = adjacencyList[startNode]

                if startNode not in vertices:
                    vertices.append(startNode)  

            # Once we hit a connected component, we start populating DAT QUEUE.
            for neighbor in neighbors:
                edge = (startNode, neighbor)
                if neighbor not in vertices:
                    vertexQueue.put(edge)

                    vertices.append(neighbor)
                    edges.append(edge)

        # Occurs if there already is stuff inside the Queue.
        else:
            currEdge = vertexQueue.get()
            srcNode = currEdge[0]
            destNode = currEdge[1]

            # Both nodes should technically be inside the array.
            nextNeighbors = adjacencyList[destNode]

            # There should always be neighbors in this case.
            for neighbor in nextNeighbors:
                edge = (destNode, neighbor)
                if neighbor not in vertices:
                    vertexQueue.put(edge)

                    vertices.append(neighbor)
                    edges.append(edge)

    return (treeEdges, treesAdjList)

# Using minimum spanning trees, we will be finding the bridge vertices.
# This uses Tarjan's algorithm.
def findBridges(adjacencyList):
    # First, we need to find the minimum spanning trees
    spanEdges, spanTrees = findMinSpanTrees(adjacencyList)

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

    bridgeNodes = findBridges(adjacencyList)

if __name__ == '__main__':

    # If the number of arguments isn't correct, we print a usage thing.
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "GRAPH.json [ITERATIONS]\n" \
              "Example: python", sys.argv[0], "2.5.1.json"
        sys.exit()

    if len(sys.argv) == 3:
        rounds = int(sys.argv[2])
        run(rounds = rounds)
    else:
        run()