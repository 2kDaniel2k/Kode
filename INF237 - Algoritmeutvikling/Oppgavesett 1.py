
Python 3:

#! /usr/bin/python3
import sys
 
for line in sys.stdin:
    data = int(line)
    print(data)

HUSK Å PRINTE OUTPUT!

#   Autori

import sys

def initialer():
    data = sys.stdin.readline().strip()

    streng = ""
    for n in data:
        if n == n.upper():
            streng += n
    print(streng)

# Alternativt
def initialer(linje):
    return ''.join([n for n in linje if n == n.upper()])

#   Pizza crust

import sys
import math

def ost():
    data = sys.readline().strip()
    R, C = map(int, data.split())
    
    pizza_areal = math.pi * (R**2)
    oste_del = math.pi * ((R-C)**2)
    ost_prosent = (oste_del / pizza_areal) * 100
    resultat = round(ost_prosent, 9)

    print(resultat)


#   Keyboardd

import sys

def keyboardd():
    data = sys.stdin.read().strip()
    linjer = data.splitlines()
    s = linjer[0]
    t = linjer[1]
    
    antall_s = {}
    for bokstav in s:
        antall_s[bokstav] = antall_s.get(bokstav, 0) + 1

    antall_t = {}
    for bokstav in t:
        antall_t[bokstav] = antall_t.get(bokstav, 0) + 1

    sticky = set()
    for bokstav, frekvens_s in antall_s.items():
        frekvens_t = antall_t.get(bokstav, 0)
        if frekvens_s < frekvens_t:
            sticky.add(bokstav)

    print("".join(sticky))


#   Fishmongers

import sys

def monies():
    data = sys.stdin.read().strip()
    linjer = data.splitlines()
    
    tilbudsmengde, kjøpere = map(int, linjer[0].split())
    fiskevekt = list(map(int, linjer[1].split()))
    sortert_fiskevekt = sorted(fiskevekt, reverse = True)
    ettersporsel = []
    for linje in linjer[2:]:
        ettersporselsmengde, pris = map(int, linje.split())
        ettersporsel.append((ettersporselsmengde, pris))
    sortert_ettersporsel = sorted(ettersporsel, key =lambda x: x[1], reverse = True)

    tjent = 0
    i = 0
    j = 0
        
    while tilbudsmengde >= 0 and i < len(sortert_ettersporsel):
        if tilbudsmengde > sortert_ettersporsel[i][0]:
            tjent += sum(sortert_fiskevekt[j : j+sortert_ettersporsel[i][0]]) * sortert_ettersporsel[i][1]
            tilbudsmengde -= sortert_ettersporsel[i][0]
            j += sortert_ettersporsel[i][0]
            i += 1
        else:
            tjent += sum(sortert_fiskevekt[j : j + tilbudsmengde]) * sortert_ettersporsel[i][1]
            j += tilbudsmengde
            tilbudsmengde = 0
            break

    print(tjent)

#   Contest struggles

import sys

def vanskeligheter():
    data = sys.stdin.read().strip()
    linjer = data.splitlines()

    n, k = map(int, linjer[0].split())
    d, s = map(int, linjer[1].split())
    resultat = round(((n*d)-(k*s)) / (n-k), 9)
    
    if 0 <= resultat <= 100:
        print(resultat)
    else:
        print("impossible")



Python 3:

#! /usr/bin/python3
import sys
 
for line in sys.stdin:
    data = int(line)
    print(data)

HUSK Å PRINTE OUTPUT!








































    
