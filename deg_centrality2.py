import json
import sys
from pprint import pprint
import heapq
'''
strategy designed to beat max degree ta

Take top 1 to n-1 nodes in terms of degree and
one node adjacent to highest degree node

Should result in pick clashes on 1 to n-1 highest degree nodes
so TA will get the nth degree node, and we will get the 1st highest
degree node.
'''

def run(NUM_ROUNDS = 1):
    # This is the JSON file that will be parsed.
    file = sys.argv[1]
    info = file.split('.')
    num_players = int(info[0])
    num_seeds = int(info[1])
    graph_id = int(info[2])

    with open(file) as data_file:
        data = json.load(data_file)

    # do degree centrality for now
    top = []
    adj_list = []

    myfile = open("deg_centrality2.txt", "w")

    # This is each node/neighbor pair.
    for key, val in data.iteritems():

        centrality = len(val)

        if len(top) < num_seeds:
            if len(val) > len(adj_list):
                # Trying to get the adjacency list of the highest
                # degree.
                adj_list = val

            # This heap is used to sort quickly and to store minimum easily.
            heapq.heappush(top, (centrality, key))

        # If we find something larger than the minimum, we pop that and push
        # the new value.
        elif centrality > top[0][0]:
            if len(val) > len(adj_list):
                adj_list = val
            heapq.heappop(top)
            heapq.heappush(top, (centrality, key))

    # Selecting the right nodes.
    for i in range(len(top)):
        top[i] = [top[i][0], int(top[i][1])]
    top.sort(reverse = True)
    top[-1] = [-1, adj_list[0]]

    for i in range(NUM_ROUNDS):
        for centrality, node in top:
            myfile.write("%d,%d\n" %(int(node),int(centrality)))



    # # add first neighbor of the largest
    # top[-1] = [-1, int(top[-1][2][0])]
    # for i in range(len(top)):
    #     print top[i][1]
    #     myfile.write("%d\n" %(int(top[i][1])))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "graph_filename.json \n" \
            "Example: python", sys.argv[0], "2.5.1.json"
        sys.exit()

    rounds = 50
    if len(sys.argv) == 3:
        rounds = int(sys.argv[2])
    run(NUM_ROUNDS = rounds)

