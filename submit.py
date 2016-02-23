import sys
import subprocess
import random


if len(sys.argv) < 2:
    print "Usage: python submit.py graph_filename.json strat1 strat2 ..."
    sys.exit()

NUM_ROUNDS = 50

# This represents the graph JSON file.
file = sys.argv[1]

# This represents the python files that represent our 
# strategies.
strats = sys.argv[2:]

# We want to find the number of iterations. Using integer diviosn
# we try to arrive at a mixed strategy. "Iter" will be the number of 
# times we invoke a particular strategy.
iter = NUM_ROUNDS / len(strats)

# This will be our submission file we write to.
myfile = open("submit.txt", "w")

# We see if integer division is clean. If not, we have to add
# some other strategies.
j = iter * len(strats)

# For each strategy, we run it ''iter'' times.
for i in range(len(strats)):

    # Arguments:
    # arg0 = "python"
    # arg1 = python file
    # arg2 = json file
    # arg3 = number of iterations.
    subprocess.call(["python", strats[i], sys.argv[1], str(iter)])

    # Writing output.
    for line in open('output.txt'):
        myfile.write(line)

if j < NUM_ROUNDS:
    # Pick one of the strats at random
    subprocess.call(["python", random.choice(strats), sys.argv[1], str(50-j)])
    for line in open('output.txt'):
        myfile.write(line)

