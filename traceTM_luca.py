#!/usr/bin/python3
import csv
import sys

class turing:

    def __init__(self, name, start, accept, reject, trans):
        self.name = name
        self.start = start
        self.accept = accept
        self.reject = reject
        self.trans = trans

def create_ntm(filename):
    file = open(filename, 'r')
    trans = []
    name = ""
    start = ""
    accept = ""
    reject = ""
    for index, row in enumerate(file):
        if index == 0:
           name = row.strip() 
        elif index == 4:
           start = row.strip()
        elif index == 5:
            accept = row.strip()
        elif index == 6:
            reject = row.strip()
        elif index > 6:
            trans.append(row.strip())
           # trans.append(row.strip().replace("_", ""))

    return turing(name, start, accept, reject, trans)

def main():
    #create ntm and take command line arguments
    ntm = create_ntm(sys.argv[1].strip())
    string = sys.argv[2]
    term = int(sys.argv[3])
    tree = []

    #begin tree with starting configuration
    cur = ntm.start
    tree.append([["___", cur, string + "___", "START"]])
    i = 0 #depth of tree
    ts = 0 #number of transitions made
    accepted = 0 #flag for whether string was accepted

    #loop through simulation
    while (i < len(tree)) and (i < term): #
        new = []
        for state in tree[i]: #for each possible state after n transitions...
            for t in ntm.trans:
                if (t.split(",")[0] == state[1]) and (t.split(",")[1] == state[2][0:1]): #...look for all possible transitions away
                    ts += 1

                    #create new config based on direction and current string state
                    if t.split(",")[4].strip() == "R": 
                        new.append([state[0] + t.split(",")[3].strip(), t.split(",")[2], state[2][1:], state[:-1]])
                    elif t.split(",")[4].strip() == "L":
                        new.append([state[0][:-1], t.split(",")[2], state[0][-1:] + t.split(",")[3].strip() + state[2][1:], state[:-1]])

                    #if state is accepted, halt simulation
                    if new[-1][1] == ntm.accept: 
                        accepted = 1
                        break
            
            if accepted == 1: break
        
        #if any new configurations are possible
        if len(new) > 0:
            tree.append(new)
        if accepted == 1: break

        i = i+1

    #print output
    print(f"Machine name: {ntm.name:>20}")
    print(f"Initial string: {string:>15}")
    print(f"Tree depth: {len(tree):>17}")
    print(f"Transitions simulated: {ts:>7}")

    #if limit reached
    if i == term: 
        print(f"Execution stopped after {i} transitions")
        return

    #output if accepted
    if accepted == 1:
        path = []
        print(f"String accepted in: {len(tree):>9}")

        #backtrack to find path taken
        ccur = tree[-1][-1][-1]
        path.append(tree[-1][-1][:-1])
        tree.reverse()

        #loop through tree, backwards
        for index, level in enumerate(tree[1:]):

            #if start state has been reached, append and break
            if index == len(tree): 
                path.append(level[0])
                break
            
            #loop through states at each level and append if it was taken
            for c in level:
                if c[:-1] == ccur: 
                    path.append(c[:-1])
                    ccur = c[-1]

        #output path
        path.reverse()
        print("Path taken:")
        for i in path:
            print(i)

        tree.reverse()
    else:
        #if not accepted
        print(f"String rejected in: {len(tree):>9}")

    total = 0

    #calculate degree of nondeterminism
    for ind in range(1, len(tree)):
        total += len(tree[ind])/len(tree[ind-1]) 
    total += 1 #account for starting configuration not coming from anything
    dindex = total/len(tree)

    print(f"Degree of non-determinism: {dindex}")

if __name__ == "__main__":
    main()
    



