import json
import sys
from pprint import pprint
import heapq
import Queue
import copy
from tqdm import *

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

# This is called to remove bridge edges from a graph, so we just have a collection
# of strongly connected components.

# Apparently, some edges go to themselves. Lol. I'm removing those too.
def removeEdges(edges, adjList):
    for edge in edges:
        node1 = edge[0]
        node2 = edge[1]

        # Forward direction:
        if node1 in adjList:
            neighbors = adjList[node1]
            neighbors.remove(node2)

            # Removing edges that go to itself: These
            # aren't bridge edges.
            if node1 in neighbors:
                neighbors.remove(node1)

            adjList[node1] = neighbors

        # Backwards direction:
        if node2 in adjList:
            neighbors = adjList[node2]
            neighbors.remove(node1)

            if node2 in neighbors:
                neighbors.remove(node2)

            adjList[node2] = neighbors 

        # Removing empty keys.
        if len(adjList[node1]) == 0:
            del(adjList[node1])

        if len(adjList[node2]) == 0:
            del(adjList[node2])

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

    stack.append(("ROOT", startNode))

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
            stack.append("DONE")
            stack.append(("ROOT", startNode))
            # Once we hit a connected component, we start populating DAT QUEUE.
            for neighbor in neighbors:
                edge = (startNode, neighbor)
                if neighbor not in vertices:
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

    # bridgeEdges
    bridgeEdges = []

    for edgeIdx in range(len(spanEdges)):
        edges = spanEdges[edgeIdx]
        treeList = spanTrees[edgeIdx]
        orderedVertices = preOrderVertices(edges, numVertices)
        spanOrderedVerts.append(orderedVertices)

        NDVertices = ND(orderedVertices, treeList)

        # Now, the lower and higher bounds.
        orderedMap = vertToList(orderedVertices)

        lowerBoundVertices = lowerBound(orderedVertices, orderedMap, \
                                        adjacencyList, treeList)
        lowerBoundVertices.sort()

        higherBoundVertices = higherBound(orderedVertices, orderedMap, \
                                        adjacencyList, treeList)
        higherBoundVertices.sort()

        # Last step...
        bridgeNodes, bridgeEdge = getBridgeVertices(NDVertices, lowerBoundVertices, \
                                        higherBoundVertices, treeList,
                                        orderedMap)
        print len(bridgeNodes)
        bridges.append(bridgeNodes)
        bridgeEdges.append(bridgeEdge)

    return (bridges, bridgeEdges)

# This will just output the bridge vertices. This does the
# check to see if a vertex is indeed a bridge vertex.
def getBridgeVertices(ND, LB, HB, adjList, ordMap):
    bridgeNodes = []
    bridgeEdges = []
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
                neighborND = ND[order - 1][2]
                neighborLB = LB[order - 1][2]
                neighborHB = HB[order - 1][2]

                if neighborLB == order and \
                   neighborHB < order + neighborND:
                    bridgeEdge = (vertex, neighbor)
                    if vertex not in bridgeNodes:
                        bridgeNodes.append(vertex)

                    if neighbor not in bridgeNodes:
                        bridgeNodes.append(neighbor)

                    if bridgeEdge not in bridgeEdges:
                        bridgeEdges.append(bridgeEdge)

    return (bridgeNodes, bridgeEdges)


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

# Simply put, this will just output a new dictionary with altered values.
# that don't include the values from sourceDict.
# We're assuming that edittedDict is undirected, while sourceDict is 
# directed.
def removeKeyValue(sourceDict, edittedDict):
    newDict = copy.deepcopy(edittedDict)
    for key, vals in sourceDict.iteritems():
        # Forward
        values = newDict[key]

        for val in vals:
            values.remove(val)

        if len(values) == 0:
            del(newDict[key])
        else:
            newDict[key] = values

        # Backward
        for val in vals:
            nextValues = newDict[val]
            nextValues.remove(key)

        if len(nextValues) == 0:
            del(newDict[val])
        else:
            newDict[val] = nextValues

    return newDict

# This just finds the smallest preOrder ranking for each of the 
# adjacent things.
def lowerBound(orderedVertices, orderedMap, adjacencyList, treeList):

    # Once again, we'll use dynamic programming.

    # Since we want minimums, we set all initial values to be the
    # size of the vertices.
    numVertices = len(orderedVertices)
    lowBounds = [numVertices] * numVertices

    lowBoundVertices = []

    # "Red Edge" adjacency list
    redAdjList = removeKeyValue(treeList, adjacencyList)

    # We're going in post order boyssssssssssss
    orderedVertices.sort(reverse = True)

    for orderedVertex in orderedVertices:
        vertex = orderedVertex[1]
        lowBound = orderedVertex[0]

        # First, check the current red edges.
        if vertex in redAdjList:
            neighbors = redAdjList[vertex]

            for neighbor in neighbors:

                # All vertices in orderedVert are connected, so it should
                # have some sort of entry in orderedMap.
                tempVal = orderedMap[neighbor]
                if lowBound > tempVal:
                    lowBound = tempVal

        # Then, dynamic programming
        if vertex in treeList:
            # Use dynamic programming yoo
            treeChildren = treeList[vertex]

            for children in treeChildren:
                childLowBound = lowBounds[int(children)]
                if lowBound > childLowBound:
                    lowBound = childLowBound

        lowBounds[int(vertex)] = lowBound
        lowBoundTuple = (orderedVertex[0], vertex, lowBound)
        lowBoundVertices.append(lowBoundTuple)

    return lowBoundVertices

# This just finds the highest preOrder ranking for each of the 
# adjacent things.
def higherBound(orderedVertices, orderedMap, adjacencyList, treeList):

    # Once again, we'll use dynamic programming.

    # Since we want maximums, we set all initial values to be 1.
    numVertices = len(orderedVertices)
    highBounds = [1] * numVertices

    highBoundVertices = []

    # "Red Edge" adjacency list
    redAdjList = removeKeyValue(treeList, adjacencyList)

    # We're going in post order boyssssssssssss
    orderedVertices.sort(reverse = True)

    for orderedVertex in orderedVertices:
        vertex = orderedVertex[1]
        highBound = orderedVertex[0] # Sticking with preOrder.

        # First, check the current red edges.
        if vertex in redAdjList:
            neighbors = redAdjList[vertex]

            for neighbor in neighbors:

                # All vertices in orderedVert are connected, so it should
                # have some sort of entry in orderedMap.
                tempVal = orderedMap[neighbor]
                if highBound < tempVal:
                    highBound = tempVal

        # Then, dynamic programming
        if vertex in treeList:
            # Use dynamic programming yoo
            treeChildren = treeList[vertex]

            for children in treeChildren:
                childHighBound = highBounds[int(children)]
                if highBound < childHighBound:
                    highBound = childHighBound

        highBounds[int(vertex)] = highBound
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


    outFile = open("bridgeNodes.txt", "w")

    bridgeNodes, bridgeEdges = findBridges(adjacencyList)

    topBridges = bridgeRanking(bridgeNodes, bridgeEdges, adjacencyList)

    for bridge in topBridges:
        bridgeNodeID = bridge[1]
        outFile.write(str(bridgeNodeID) + "\n")

# This is called after finding bridges. The idea is to find a way to measure the
# significance of some bridge nodes. We do this by searching through ALL the nodes 
# that we found, and storing the respective size of the partition that they hold.
def bridgeRanking(bridgeNodes, bridgeEdges, adjacencyList):
    bridges = []
    edges = []
    numVertices = len(adjacencyList.keys())
    sortedBridges = []
    cutList = copy.deepcopy(adjacencyList)

    # Unpacking all of the different components.
    for bridge in bridgeNodes:
        for node in bridge:
            bridges.append(node)

    # Unpacking all the edges
    for edge in bridgeEdges:
        for cut in edge:
            edges.append(cut)


    # Removing the appropriate edges
    cutList = removeEdges(edges, cutList)

    # Now, searching via each node.
    for nodeID in tqdm(range(len(bridges))):
        node = bridges[nodeID]

        if numVertices < 1000:
            sizeOfComponent = dfs(node, cutList)

        else:
            sizeOfComponent = dfs(node, cutList, depth = 1500)
        remainingPart = numVertices - sizeOfComponent
        if node in cutList:
            degree = len(cutList[node])
        else:
            degree = 0

        # We are measuring by doing degree/partition size.
        # The larger the value, the more valuable.
        partitionBridge = (2 * degree + sizeOfComponent / \
                           float(sizeOfComponent * remainingPart), node)
        sortedBridges.append(partitionBridge)

        # If the graph is too large, we need to tradeoff and just look at
        # degrees for sorting.
    sortedBridges.sort(reverse = True)

    return sortedBridges


# The algorithm here is almost identical to that of the minimum spanning 
# Tree. Look at the code for that to understand this.
def dfs(node, adjList, depth = None):
    stack = []
    stack.append("DONE")
    stack.append(("Root",node))
    vertices = []
    vertices.append(node)

    # If this is the case, then the size of partition is just 1 lol.
    if node not in adjList:
        return len(vertices)

    else:
        neighbors = adjList[node]

        for neighbor in neighbors:
            if neighbor not in vertices:
                currEdge = (node, neighbor)
                vertices.append(neighbor)
                break

        while currEdge != "DONE":

            srcNode = currEdge[0]
            destNode = currEdge[1]

            nextNeighbors = adjList[destNode]
            unVisitedNeighbor = False

            for nextNeighbor in nextNeighbors:
                if nextNeighbor not in vertices:
                    stack.append(currEdge)
                    vertices.append(nextNeighbor)
                    currEdge = (destNode, nextNeighbor)
                    unVisitedNeighbor = True
                    break

            if unVisitedNeighbor == False:
                currEdge = stack.pop()

            if depth != None:
                if depth <= len(vertices):
                    return len(vertices)

    return len(vertices)



if __name__ == '__main__':

    # If the number of arguments isn't correct, we print a usage thing.
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "GRAPH.json [ITERATIONS]\n" \
              "Example: python", sys.argv[0], "2.5.1.json"
        sys.exit()

    print "Finding the bridges..."

    if len(sys.argv) == 3:
        rounds = int(sys.argv[2])
        run(rounds = rounds)
    else:
        run()