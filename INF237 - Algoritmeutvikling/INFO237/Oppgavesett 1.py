#   Autori

import sys

def initialer():
    data = sys.stdin.readline().strip()

    streng = ""
    for n in data:
        if n.isalpha() and n.isupper():
            streng += n
    print(streng)

initialer()

#   Pizza crust

import sys
import math

def ost():
    data = sys.stdin.readline().strip()
    R, C = map(int, data.split())           #R er pizza radius i cm, C er crusten i cm
    
    pizza_areal = math.pi * (R**2)
    oste_del = math.pi * ((R-C)**2)
    ost_prosent = (oste_del / pizza_areal) * 100
    resultat = round(ost_prosent, 9)

    print(resultat)

ost()


#   Keyboardd

import sys

def keyboardd():
    data = sys.stdin.read().strip()
    linjer = data.splitlines()
    s = linjer[0]   #Hva som var ment til å bli skrevet
    t = linjer[1]   #Hva som ble skrevet
    
    antall_s = {}   #Telle forekomster av hver bokstav i s i fortegnelseformat
    for bokstav in s:
        antall_s[bokstav] = antall_s.get(bokstav, 0) + 1

    antall_t = {}
    for bokstav in t:   #Tilsvarende for t
        antall_t[bokstav] = antall_t.get(bokstav, 0) + 1

    sticky = set()  #Sammenligne forekomster av hver bokstav i begge fortegnelser
    for bokstav, frekvens_s in antall_s.items():
        frekvens_t = antall_t.get(bokstav, 0)
        if frekvens_s < frekvens_t:
            sticky.add(bokstav)

    print("".join(sticky))

keyboardd()

#   Fishmongers

import sys

def monies():
    data = sys.stdin.read().strip()
    linjer = data.splitlines()
    
    tilbudsmengde, kjøpere = map(int, linjer[0].split())
    fiskevekt = list(map(int, linjer[1].split()))
    sortert_fiskevekt = sorted(fiskevekt, reverse = True)   #Sortert fallende liste av fiskevekt
    ettersporsel = []
    for linje in linjer[2:]:
        ettersporselsmengde, pris = map(int, linje.split())
        ettersporsel.append((ettersporselsmengde, pris))
    sortert_ettersporsel = sorted(ettersporsel, key =lambda x: x[1], reverse = True) #Sortert fallende etter pris

    tjent = 0
    i = 0
    j = 0
        
    while tilbudsmengde >= 0 and i < len(sortert_ettersporsel): #Så lenge BÅDE tilbud og etterspørsel finnes
        if tilbudsmengde > sortert_ettersporsel[i][0]:
            tjent += sum(sortert_fiskevekt[j : j+sortert_ettersporsel[i][0]]) * sortert_ettersporsel[i][1]  #Summe antall fisk fiskeren ønsker å kjøpe med kilopris, prioriterer tyngste fisk (tilbud)
            tilbudsmengde -= sortert_ettersporsel[i][0]
            j += sortert_ettersporsel[i][0]
            i += 1
        else:   #Når det er færre fisk enn etterspørsel
            tjent += sum(sortert_fiskevekt[j : j + tilbudsmengde]) * sortert_ettersporsel[i][1] #Tilsvarende if-funksjonen, bare at vi multipliserer resterende tilbud fremfor ep til fiskeren.
            j += tilbudsmengde
            tilbudsmengde = 0
            break

    print(tjent)

monies()

#   Contest struggles

import sys

def vanskeligheter():
    data = sys.stdin.read().strip()
    linjer = data.splitlines()

    n, k = map(int, linjer[0].split())
    d, s = map(int, linjer[1].split())
    resultat = round(((n*d)-(k*s)) / (n-k), 9)  #Formel for forventet output
    
    if 0 <= resultat <= 100:    #Dersom gjennomsnittlig vanskelighet for gjenstående problemer er innenfor [0, 100], er inputet gyldig
        print(resultat)
    else:
        print("impossible")

vanskeligheter()