#!/usr/bin/python

import sys
chains = 2077
n = 0
chainids=["A","B"]

with open(sys.argv[1],'r') as f:
    for line in f:
        if line.startswith("END") or line.startswith("TER"):
            break
        chains += 1

with open(sys.argv[1],'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('ATOM'):
            n=n+1
            tmp = list(line)
            if n>chains: 
                tmp[21] = chainids[1]
            else:
                tmp[21] = chainids[0]
            line = "".join(tmp)
        print line
