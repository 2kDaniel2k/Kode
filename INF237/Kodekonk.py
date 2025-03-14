import sys
from collections import defaultdict

def Bernie():
    data = sys.stdin.read().splitlines()
    n = int(data[0])

    dict = defaultdict(list)

    for tur in data[1: n + 1]:
        land, år = tur.split()
        år = int(år)
        dict[land].append(år)
    
    for key in dict.keys():
        dict[key].sort()

    q = int(data[n + 1])
    spm = []
    for linje in data[n + 2]:
        land, nr = linje.split()
        nr = int(nr)
        spm.append((land, nr))

    for case in spm:
        print(dict[case[0]][case[1] - 1])


a = "4
Iceland 2016
Sweden 2015
Iceland 1982
Norway 1999
3
Sweden 1
Iceland 1
Iceland 2"

Bernie(a)
