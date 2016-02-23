import sim
import sys
import subprocess
import json

if len(sys.argv) < 2:
    print "Usage: python runSim.py graph_filename.json strat1 strat2 ..."
    sys.exit()

# file represents the JSON file.

# The JSON is in the format:
# numPlayers.numSeeds.uniqueID.json

file = sys.argv[1]
info = file.split('.')

num_players = int(info[0])
num_seeds = int(info[1])
graph_id = int(info[2])

# Python strategy files.
strats = sys.argv[2:]

# This simulation is supposed to simulate people playing against each other.
# So, we want there to be strategies for each person.
if num_players != len(strats):
    print "Usage: python runSim.py graph_filename.json strat1 strat2 ..."
    sys.exit()

# This simulation is here to simulate people playing against each other.
d = {}
for i in range(num_players):

    # Each player will invoke a call to the their particular strategy.
    subprocess.call(["python", strats[i], sys.argv[1], "1"])

    # The dictionary will then store as a key value:
    # key = [STRATEGY_NAME][PLAYERID]
    # where the STRATEGY_NAME is the python file (without the .py), and the
    # PLAYERID is the integer that corresponds to the particular player.

    # The value stored in this dictionary will be the particular output for this
    # particular strategy. This output is the adjacency list.
    d['%s%d' %(str(strats[i][:-3]), i)] = [line.rstrip('\n') for line in open('output.txt')]



with open(sys.argv[1]) as data_file:
    data = json.load(data_file)

print sim.run(data,d)
