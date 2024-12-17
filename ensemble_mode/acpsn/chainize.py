#!/usr/bin/python

import sys
fh = open(sys.argv[1],'r')

n=0
# Here add the last atom number in your PDB
chains=2077
chainids=["A","B"]

for line in fh:
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
