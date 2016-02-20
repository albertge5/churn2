import json
import sys
from pprint import pprint
import heapq


def run(NUM_ROUNDS = 50):

    file = sys.argv[1]
    info = file.split('.')
    num_players = int(info[0])
    num_seeds = int(info[1])
    graph_id = int(info[2])

    with open(file) as data_file:
        data = json.load(data_file)

    # do degree centrality for now
    top = []

    myfile = open("output.txt", "w")

    for i in range(NUM_ROUNDS):
        for key, val in data.iteritems():
            centrality = len(val)
            if len(top) < num_seeds:
                heapq.heappush(top, (centrality, key))

            elif centrality > top[0][0]:
                heapq.heappop(top)
                heapq.heappush(top, (centrality, key))

        for i in range(len(top)):
            top[i] = [top[i][0], int(top[i][1])]
        top.sort(reverse = True)
        for node, centrality in top:
            myfile.write("%d\n" %(centrality))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "graph_filename.json \n" \
            "Example: python", sys.argv[0], "2.5.1.json"
        sys.exit()

    rounds = 50
    if len(sys.argv) == 3:
        rounds = int(sys.argv[2])
    run(NUM_ROUNDS = rounds)

