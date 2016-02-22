import sys
import subprocess
import random


if len(sys.argv) < 2:
    print "Usage: python submit.py graph_filename.json strat1 strat2 ..."
    sys.exit()

NUM_ROUNDS = 50
file = sys.argv[1]
strats = sys.argv[2:]

iter = NUM_ROUNDS / len(strats)
myfile = open("submit.txt", "w")
j = iter * len(strats)
for i in range(len(strats)):
    subprocess.call(["python", strats[i], sys.argv[1], str(iter)])
    for line in open('output.txt'):
        myfile.write(line)

if j < 50:
    # pick one of the strats at random
    subprocess.call(["python", random.choice(strats), sys.argv[1], str(50-j)])
    for line in open('output.txt'):
        myfile.write(line)

