# Bracket Pairing

"""
Vi sjekker først hele strengen for gyldige par, og deretter innsnevrer vi med 1 fra begge sider for å sjekke delstrenger rekursivt.
Hopper med 2 for å sikre at det er partall antall tegn mellom åpen og lukket bracket.

Venstre og høyre delstrengene sjekkes rekursivt på følgende måte:
venstre = antall_gyldig(x + 1, i - 1)
hoyre = antall_gyldig(i + 1, y)

Eksempel: (??)

antall_gyldig(0, 3) --> i går over 1 og 3

Iterasjon 1: i = 1
data[0] = "(" og data[1] = "?" --> Siden data[0] er fast, finnes det bare en løsning for "?" (1 mulighet)

Rekursjonen (innsnevring)
Venstre del antall_gyldig(1, 0) returneres til 1 fordi basistilfellet x > y er nådd
Høyre del antall_gyldig(2, 3) med dekstrengen "??" (indeks 2 og 3 - begge inkludert)
- Gir 1 mulighet
    Rekursjon venstre del for (2, 3) --> antall_gyldige(3, 2)      antall_gyldige(1 + 1, 2 - 1)
        - Basistilfellet nådd, returnerer 1
    Rekursjon høyre del for (2, 3) --> antall_gyldige(4, 3)        antall_gyldige(2 + 2, 3)
        - Basistilfellet nådd, returnerer 1
    Resultat for antall_gyldige(2, 3) = 1 * 1 * 1 = 1
    fortegnelse[(2, 3)] = 1
muligheter (1) * venstre (1) * hoyre (1) = 1


Iterasjon 2: i = 3
data[0] = "(" og data[3] = ")" --> Siden begge de faste parene stemmer overens returneres 1 i sjekken

Rekursjonen (innsnevring)
Venstre del antall_gyldig(1, 2) med delstrengen "??" (indeks 1 og 2 - begge inkludert)
- Gir 4 muligheter
    Rekursjon venstre del for (1, 2) --> antall_gyldige(2, 1)      antall_gyldige(1 + 1, 2 - 1)
        - Basistilfellet nådd, returnerer 1
    Rekursjon høyre del for (1, 2) --> antall_gyldige(3, 2)         antall_gyldige(2 + 1, 2)
        - Basistilfellet nådd, returnerer 1
    Resultat for antall_gyldige(1, 2) = 4 * 1 * 1 = 4
    fortegnelse[(1, 2)] = 4
Høyre del antall_gyldig(4, 3) returnerer 1 fordi basistilfellet x > y er nådd
muligheter (4) * venstre (1) * hoyre (1) = 4

Iterasjon 1 (1) + Iterasjon 2 (4) = 5
"""

import sys

def bracket():
    data = sys.stdin.read().strip()
    n = len(data)   # Antall tegn i strengen
    fortegnelse = {}

    # Returnerer antall måter å få a og b til å danne et par
    # 1. Hvis begge er "?", kan vi velge en av de 4 parentes-typene --> 4 muligheter
    # 2. Hvis kun a eller b er "?", må den korrespondere med den andre --> 1 muligheter
    # 3. Hvis begge != "?", sjekk om de matcher

    def sjekk_par(a, b):
        if a == "?" and b == "?":
            return 4
        # b er fast - a må da velges som den unike åpne bracketen som matcher b
        elif a == "?":
            if b in [")", "]", "}", ">"]:
                return 1
            else:
                return 0
        # a er fast - b må da velges som den unike lukkende bracketen som matcher a
        elif b == "?":
            if a in ["(", "[", "{", "<"]:
                return 1
            else:
                return 0
        # a og b er faste - sjekk om de matcher
        else:
            par = {"(": ")", "[": "]", "{": "}", "<": ">"}
            if a in par and par[a] == b:
                return 1
            else:
                return 0

    # Teller hvor mange måter vi kan gjøre del-strengen data[x : y + 1] til en gyldig bracket-sekvens, gjennom en rekursiv funksjon
    def antall_gyldig(x, y):
        # Basistilfellet: Dersom x > y, er det ingen tegn igjen i delstrengen, og vi har en gyldig bracket-sekvens (ingen tegn, ingen feil)
        if x > y:
            return 1
        # Dersom vi har sett denne delstrengen tidligere, henter vi svaret fra fortegnelse istedenfor å regne det ut igjen
        if (x, y) in fortegnelse:
            return fortegnelse[(x, y)]
        resultat = 0    # Antall gyldige bracket-sekvenser
        # Vi itererer over alle mulige posisjoner data[x] kan matches med en lukket bracket ( ")", "]", "}", ">" )
        # Den første mulige bracketen kommer etter x, så vi starter på x + 1
        # Øker med 2 for å sikre at lengden på sekvensen forblir partall - Kan altså ikke ha et oddetall antall tegn mellom åpen og lukket bracket
        for i in range(x + 1, y + 1, 2):
            # Beregner antall måter å få data[x] og data[i] til å danne et par
            muligheter = sjekk_par(data[x], data[i])
            if muligheter > 0:
                # Innsnevrer intervallet med 1 fra både venstre og høyre gjennom to rekursive kall
                venstre = antall_gyldig(x + 1, i - 1)
                hoyre = antall_gyldig(i + 1, y)
                resultat += muligheter * venstre * hoyre
        fortegnelse[(x, y)] = resultat
        return resultat
    
    # Kaller den rekursive funksjonen antall_gyldig(x, y) med startindeks x = 0 og sluttindeks y = n - 1
    # Dette betyr at vi prøver å finne antall gyldige bracket-sekvenser for hele inputstrengen
    # Eks: (??)
    # Matche data[0] = "(", med data[1] = "?" (1 mulighet))     --> og resten må fylles ut gyldig
    # Matche data[0] = "(", med data[3] = ")" (1 mulighet)       --> og resten av strengen "??" må fylles ut gyldig
    endelig = antall_gyldig(0, n - 1)
    print(endelig)

bracket()



# Map Coloring

"""
gyldig sjekker om det er lov å bruke en spesifikk farge på et land. Går gjennom alle naboland og sjekker om de har samme farge.
kan_farge prøver å fargelegge alle landene i grafen med k farger.
Lager en adjecency graf / liste over naboland. Eks:
Adjacency-liste: En liste over noder (land) og deres naboer (grensende land). Hver node har en liste over naboene sine.
graf = [
    [1, 2],     Land 0 grenser til naboland 1 og 2
    [2],        Land 1 grenser til naboland 2
    [3],        Land 2 grenser til naboland 3
    [1]         Land 3 grenser til naboland 1
    ]
Siste kodeblokken tester fargelegging av landene med 1-4 farger. Returnerer minste mulige antall farger, eller "many" dersom det ikke er mulig.
"""

import sys

def color():
    data = sys.stdin.read().split()
    T = int(data[0])    # Antall cases
    resultater = []
    i = 1

    # Sjekker om det er lov å bruke fargen "farge" på land. Går gjennom alle naboland og sjekker om de har samme farge.

    # graf er adjacency listen over naboland
    # farger[i] er en liste som lagrer fargen til land i, hvor hver farge representeres som et heltall fra 0 til k - 1. Alle land starter med farge -1 (ingen farge).
    # land er indeksen til landet vi prøver å fargelegge
    # farge er fargen vi prøver å fargelegge landet med - heltall
    def gyldig(graf, farger, land, farge):
        for nabo in graf[land]: # Går gjennom alle naboland for landet vi prøver å fargelegge
            if farger[nabo] == farge: # Hvis nabolandet allereded har fargen vi prøver å bruke, kan vi ikke bruke fargen - returnerer False
                return False
        return True
    

    # Rekursiv backtracking-funksjon som prøver å fargelegge alle landene i grafen med k farger

    # k er antall farger vi kan bruke
    def kan_farge(graf, farger, land, k):
        if land == len(graf):
            return True   # Hvis alle land har fått en farge, returner True - land er et heltall som øker med en for hver iterasjon
        # Prøver hver farge fra 0 til k - 1 på det aktuelle landet
        # Hvis fargen vi prøver er gyldig i henhold til nabolandene, prøver vi å fargelegge neste land.
        for farge in range(k):
            if gyldig(graf, farger, land, farge):
                farger[land] = farge
                if kan_farge(graf, farger, land + 1, k):    # Hvis mulig, prøver vi å fargelegge neste land på samme måte (rekursiv funksjon)
                    return True
                farger[land] = -1   # Dersom fargen er ugyldig, nullstilles fargen til det aktuelle landet (ikke alle land), og vi prøver neste farge - Dette er backtracking
        return False    # Hvis ingen fargekombinasjoner er gyldige, returner vi False

    for _ in range(T):
        C = int(data[i])    # Antall land
        B = int(data[i + 1])    # Antall grenser
        i += 2
        graf = [[] for _ in range(C)]   # Adjacency-liste (liste av lister) over naboland. Hvert indeks tilhører ett land, og innholder i listen er naboene.
        for _ in range(B):
            # u og v er indeksene til to naboland
            u = int(data[i])
            v = int(data[i + 1])
            i += 2  # Hopper til neste linje av to naboland
            # Legger til v som en nabo til u, og vice versa
            graf[u].append(v)
            graf[v].append(u)

        # Finne minste antall farger k fra 1-4 ellers returnere "many"
        minste = None
        for k in range(1, 5):   # Denne loopen stopper så snart vi har funnet et antall farger som fungerer - tester totalt 4 farger
            farger = [-1] * C   # Lager listen farger[i] som lagrer fargen til land i. Starter som sagt med -1 (ingen farge).
            if kan_farge(graf, farger, 0, k):   # Bruker kan_farge for å se om vi kan fargelegge alle landene med k farger
                minste = k
                break
        if minste is None:
            resultater.append("many")
        else:
            resultater.append(str(minste))

    sys.stdout.write("\n".join(resultater))

color()