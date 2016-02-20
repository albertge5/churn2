import sim
import sys
import subprocess
import json

if len(sys.argv) < 2:
    print "Usage: python seeds.py graph_filename.json strat1 strat2 ..."
    sys.exit()


file = sys.argv[1]
info = file.split('.')
num_players = int(info[0])
num_seeds = int(info[1])
graph_id = int(info[2])

strats = sys.argv[2:]
if num_players != len(strats):
    print "Usage: python seeds.py graph_filename.json strat1 strat2 ..."
    sys.exit()

d = {}
for i in range(num_players):
    subprocess.call(["python", strats[i], sys.argv[1], "1"])
    d['%s%d' %(str(strats[i][:-3]), i)] = [line.rstrip('\n') for line in open('output.txt')]



with open(sys.argv[1]) as data_file:
    data = json.load(data_file)

print sim.run(data,d)
