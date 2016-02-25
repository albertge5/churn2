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

        # Since this is we want this to be directed (for bridge detection)
        if srcNode in adjList:
            adjList[srcNode].append(destNode)

        else:
            adjList[srcNode] = [destNode]

    return adjList

# This will output an adjacencyList to a JSON file. This is just to check
# the legitimacy of an adjacency list.
def listToJSON(adjacencyList):
    jsonString = json.dumps(adjacencyList)
    outFile = open("adjList", "w")
    outFile.write(jsonString)

# Like the name suggests, this simply just finds the minimum spanning tree
# of the graph.
def findMinSpanTrees(adjacencyList):
    # Since we don't really have any weights associated with each of
    # the edges, this algorithm is basically DFS. 
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

    # Stack for DFS
    stack = []

    stack.append("DONE")

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

        # The moment we can move, we stop the for loop.
        if neighbor not in vertices:
            currEdge = edge
            vertices.append(neighbor)
            edges.append(edge)
            break

    while len(vertices) != numVertices:
        # Two cases here:
        # 1: The stack is now empty (we exhausted this component)
        #       We first make an adjacency matrix for this.
        #       In this case, we keep incrementing startIdx until
        #       we encounter an unvisited connected component.
        #
        # 2: The stack is not empty
        #       In this case, we just keep going through that component.
        if currEdge == "DONE":
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
                    stack.append("DONE")
                    currEdge = edge
                    vertices.append(neighbor)
                    edges.append(edge)
                    break

        # Occurs if there already is stuff inside the Queue.
        else:
            srcNode = currEdge[0]
            destNode = currEdge[1]

            # Both nodes should technically be inside the array.
            nextNeighbors = adjacencyList[destNode]
            # There should always be neighbors in this case.
            unVisitedNeighbor = False

            for neighbor in nextNeighbors:
                edge = (destNode, neighbor)
                if neighbor not in vertices:
                    stack.append(currEdge)
                    currEdge = edge
                    vertices.append(neighbor)
                    edges.append(edge)
                    unVisitedNeighbor = True
                    break

            if unVisitedNeighbor == False:
                currEdge = stack.pop()

    # This is for the last connected component.
    treeEdges.append(edges)
    adjList = createAdjList(edges)
    treesAdjList.append(adjList)

    return (treeEdges, treesAdjList)

# Ordering the vertices so that we can do the bridge algorithm well.
def preOrderVertices(edges, numVertices):
    # Since the edges are preordered, we just go through the edges.

    # Just to ensure that we got all the vertices.
    vertices = []

    # Return value. This list will hold tuples; first index holding the 
    # order of the vertex. Second index holding the id of the node.
    orderedVertices = []

    # Starting order:
    orderIdx = 1

    # Starting with the root node.
    rootEdge = edges[0]
    rootVert = rootEdge[0]

    # Creating the tuple
    orderedVertex = (orderIdx, rootVert)

    # Adding it to the lists so we can keep track of the met vertices.
    vertices.append(rootVert)
    orderedVertices.append(orderedVertex)

    for edge in edges:
        srcVert = edge[0]
        destVert = edge[1]
        if destVert not in vertices:
            orderIdx += 1
            orderedVertex = (orderIdx, destVert)
            vertices.append(destVert)
            orderedVertices.append(orderedVertex)

    return orderedVertices

# Using minimum spanning trees, we will be finding the bridge vertices.
# This uses Tarjan's algorithm.
def findBridges(adjacencyList):
    # Getting the the total number of vertices:
    numVertices = len(adjacencyList.keys())

    # First, we need to find the minimum spanning trees
    spanEdges, spanTrees = findMinSpanTrees(adjacencyList)
    listToJSON(spanTrees[0])

    # This is for ordered vertices for each of the connected components.
    spanOrderedVerts = []

    # These are the bridges for each of the connected components
    bridges = []

    for edgeIdx in range(len(spanEdges)):
        edges = spanEdges[edgeIdx]
        treeList = spanTrees[edgeIdx]
        orderedVertices = preOrderVertices(edges, numVertices)
        spanOrderedVerts.append(orderedVertices)

        NDVertices = ND(orderedVertices, treeList)

        # Now, the lower and higher bounds.
        orderedMap = vertToList(orderedVertices)

        lowerBoundVertices = lowerBound(orderedVertices, orderedMap, \
                                        adjacencyList)

        higherBoundVertices = higherBound(orderedVertices, orderedMap, \
                                        adjacencyList)

        # Last step...
        bridgeNodes = getBridgeVertices(NDVertices, lowerBoundVertices, \
                                        higherBoundVertices, treeList,
                                        orderedMap)
        print len(bridgeNodes)
        bridges.append(bridgeNodes)

    return bridges


def getBridgeVertices(ND, LB, HB, adjList, ordMap):
    bridgeNodes = []

    # numVertices; apparently I'm supposed to go post order...

    numVertices = len(ordMap.keys())
    # All ND, LB, HB, are ordered the same way: increasing in preorder.
    for idx in range(len(ND)):
        NDVertex = ND[idx]
        vertex = NDVertex[1]

        if vertex in adjList:
            neighbors = adjList[vertex]

            for neighbor in neighbors:
                order = ordMap[neighbor] # This starts at 1, we are 0-indexed.
                order = numVertices - order # Now, we going postorder lol.

                neighborND = ND[order - 1][2]
                neighborLB = LB[order - 1][2]
                neighborHB = HB[order - 1][2]

                if order - neighborND < neighborLB and \
                   neighborHB <= order:
                    if vertex not in bridgeNodes:
                        bridgeNodes.append(vertex)

                    if neighbor not in bridgeNodes:
                        bridgeNodes.append(neighbor)
        else:
            if vertex not in bridgeNodes:
                bridgeNodes.append(vertex)

    return bridgeNodes




# From bottom up, we will have the ND values for each vertex.
# Each ND value is equal to the sum of the values of the children
# underneath, + 1 for the current node.
# This also requires some sorting.
def ND(orderedVertices, adjacencyList):
    # This will require some dynamic programming.
    memoizeTable = [0] * len(orderedVertices)

    # Returning tuples of size 3, which include preorder, vertexId, and ND
    # value.
    NDVertices = []

    # Sorting so that we go through from children to parents.
    # This is because parents have a smaller thing than children.
    orderedVertices.sort(reverse = True)

    for orderedVertex in orderedVertices:
        vertex = orderedVertex[1]
        vertexIdx = int(vertex)

        # Not a key.
        if vertex not in adjacencyList:
            memoizeTable[vertexIdx] = 1

        else:
            neighbors = adjacencyList[vertex]
            aggregateND = 0
            for neighbor in neighbors:
                neighborIdx = int(neighbor)
                aggregateND += memoizeTable[neighborIdx]
            aggregateND += 1
            memoizeTable[vertexIdx] = aggregateND

    # Returning this in pre-ordered order.
    orderedVertices.sort()

    # Returning list of 3-tuples.
    for orderedVertex in orderedVertices:
        vertex = orderedVertex[1]
        NDVertex = (orderedVertex[0], vertex, memoizeTable[int(vertex)])
        NDVertices.append(NDVertex)

    return NDVertices

# Simply put, the orderedVertices will be made into
# a map, for easier lower/higher calculations.
def vertToList(orderedVertices):
    # This should be in increasing order.
    # We will have key = vertex
    # and value = preorder rank.

    preOrderMap = {}

    for orderedVert in orderedVertices:
        vertex = orderedVert[1]
        order = orderedVert[0]
        preOrderMap[vertex] = order

    return preOrderMap

# This just finds the smallest preOrder ranking for each of the 
# adjacent things.
def lowerBound(orderedVertices, orderedMap, adjacencyList):

    lowBoundVertices = []

    for orderedVertex in orderedVertices:
        vertex = orderedVertex[1]
        lowBound = orderedVertex[0]

        neighbors = adjacencyList[vertex]

        for neighbor in neighbors:

            # All vertices in orderedVert are connected, so it should
            # have some sort of entry in orderedMap.
            tempVal = orderedMap[neighbor]
            if lowBound > tempVal:
                lowBound = tempVal

        lowBoundTuple = (orderedVertex[0], vertex, lowBound)
        lowBoundVertices.append(lowBoundTuple)

    return lowBoundVertices

# This just finds the highest preOrder ranking for each of the 
# adjacent things.
def higherBound(orderedVertices, orderedMap, adjacencyList):

    highBoundVertices = []

    for orderedVertex in orderedVertices:
        vertex = orderedVertex[1]
        highBound = orderedVertex[0]

        neighbors = adjacencyList[vertex]

        for neighbor in neighbors:

            # All vertices in orderedVert are connected, so it should
            # have some sort of entry in orderedMap.
            tempVal = orderedMap[neighbor]
            if highBound < tempVal:
                highBound = tempVal

        highBoundTuple = (orderedVertex[0], vertex, highBound)
        highBoundVertices.append(highBoundTuple)

    return highBoundVertices

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

    outFile = open("bridgeNodes.txt", "w")
    outFile.write(str(bridgeNodes))

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