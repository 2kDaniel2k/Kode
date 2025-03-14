# Hensikten med dfs er å sjekke om alle noder i en graf er tilgjengelige fra en vilkårlig startnode.
# Graf er en adjecency list (liste av lister med naboene til hver node), start er den vilkårlige
# startnoden, og visited er en liste som holder styr på hvilke noder som er besøkt (liste med boolske
# verdier, indeksert likt adjacency listen). Hvis alle noder ikke kan besøkes vil en eller flere av
# elementene i listen være False.
def dfs(graf, start, besokt):
    stack = [start]
    while stack:
        node = stack.pop()  #Last in first out (LIFO) henter siste element i stacken
        if not besokt[node]:
            besokt[node] = True
            for neighbor in graf[node]:
                if not besokt[neighbor]:
                    stack.append(neighbor)

# Bruker dfs til å sjekke om alle noder i grafen er tilgjengelige fra startnoden 0.
def er_strongly_connected(n, graf):
    besokt = [False] * n
    dfs(graf, 0, besokt)
    if not all(besokt):
        return False

# Reverserer alle kantene i grafen, og sjekker om alle noder er tilgjengelige fra startnoden 0.
# Lager først en tom adjecency liste for den reverserte grafen, og legger til naboene til hver node.
    reversert_graf = [[] for _ in range(n)]
    for u in range(n):  # Går gjennom hver node.
        for v in graf[u]: # Går gjennom hver nabo til noden.
            reversert_graf[v].append(u) # Reverserer kanten. I den originale grafen går kanten fra u
                                        # til v, mens i den reverserte går den fra v til u. u blir
                                        # altså lagt til i listen over naboen(e) til indeks v.

# Lager en liste over besøkte noder, som starter med å være False. Bruker så dfs på den reverserte
# grafen for å sjekke om alle noder er tilgjengelige fra startnoden 0.
    besokt = [False] * n
    dfs(reversert_graf, 0, besokt)
    return all(besokt) # Returnerer True hvis alle noder er tilgjengelige, og False ellers.

def resultat():
    import sys
    input = sys.stdin.read()
    data = input.splitlines()   # Splitter inputen på linjeskift

    case_nummer = 1 # Holder styr på hvilket testtilfelle vi er på.
    i = 0 # Holder styr på hvilken linje i inputen vi er på.
    while i < len(data):
        linje = data[i]
        m, n = map(int, linje.split())  # m = antall noder, n = antall kanter
        i += 1

        # Bygger grafen og lagrer kantene
        graf = [[] for _ in range(m)]
        kanter = []
        for _ in range(n):
            a, b = map(int, data[i].split())  # Lokasjon a og b
            graf[a].append(b)  # Legger til kanten a -> b
            kanter.append((a, b)) # Lagrer kanten som en tuple (a, b)
            i += 1

        # Sjekker om grafen er strongly connected
        if er_strongly_connected(m, graf):
            print(f"Case {case_nummer}: valid")
        else:
            fant_losning = False
            for a, b in kanter:
                # Reverserer kanten i iterasjonen midlertidig
                graf[a].remove(b)
                graf[b].append(a)

                if er_strongly_connected(m, graf):  # Sjekker om reverseringen løser problemet
                    print(f"Case {case_nummer}: {a} {b}")
                    fant_losning = True
                    break

                # Reverserer den midlertidig reverserte kanten
                graf[b].remove(a)
                graf[a].append(b)

# Hvis ingen kant kan reverseres for å gjøre grafen strongly connected, er grafen ugyldig.
            if not fant_losning:
                print(f"Case {case_nummer}: invalid")

        case_nummer += 1

resultat()


# Breaking Bad

import sys

def breaking_bad():
    data = sys.stdin.read().splitlines()
    
    n = int(data[0])    # Antall ingredienser
    ingredienser = data[1 : n+1]
    m = int(data[n+1]) # Antall umulige kombinasjoner

    graf = {ingrediens: [] for ingrediens in ingredienser}  # Lager en adjacency-liste hvor ingrediensnavnet er nøkkelen, og liste av naboer (ukompatible ingredienser) er verdien
    for i in range(m):
        u, v = data[n+2+i].split() # Indekserer fra og med umulige kombinasjoner, og splitter linjen inn i u (første ingrediens) og v (andre ingrediens)
        graf[u].append(v) # Legger til ingrediensen v i adjecency listen til u
        graf[v].append(u) # Tilsvarende er u naboen til v

    farge = {}  # Vi skal bruke coloring for å sjekke om grafen er bipartite, altså at det finnes to grupper med noder hvor hver node kan tilkobles en eller flere noder i den andre gruppen. To farger: 0 og 1
    gruppe1 = []
    gruppe2 = []

    def bfs(start):
        queue = [start] # Vilkårlig startnode
        farge[start] = 0  # Startnode får farge 0
        gruppe1.append(start)   # Legger startnoden til gruppe1

        while queue: # Kjøres så lenge queue'en ikke er tom
            node = queue.pop(0) # Henter neste node i køen (FIFO)
            for nabo in graf[node]:
                if nabo not in farge:   # Hvis naboen ikke er fargelagt enda, fargelegg
                    farge[nabo] = 1 - farge[node]   # Tilordner naboen motsatt farge av nåværende node
                    if farge[nabo] == 0:    # Legger noden til i gruppe 1 eller 2, avhengig av fargen
                        gruppe1.append(nabo)
                    else:
                        gruppe2.append(nabo)
                    queue.append(nabo)  # Legger naboen til køen
                elif farge[nabo] == farge[node]: # Dersom naboer har samme farge er grafen ikke bipartite, og følgelig returneres False
                    return False

        return True # Dersom bredde-først-søket kjøres hele veien uten problemer, har vi en bipartite graf

    # Det kan hende inputet består av en graf med to eller flere komponenter (klynger med noder som er sammenkoblet) som er uavhengig av hverandre, følgelig må vi sjekke for hver slik gruppering om
    # de er bipartite. Dersom en av de ikke er det, er hele grafen uløselig.
    for ingrediens in ingredienser:
        if ingrediens not in farge:
            if not bfs(ingrediens): # Kaller bfs-funksjonen for gjeldende node (ingrediens) dersom den enda ikke har blitt besøkt. Returnerer False hvis grafen ikke er bipartite.
                print("impossible")
                return

    print(" ".join(gruppe1))    # Printer handlelisten for person 1
    print(" ".join(gruppe2))    # Tilsvarende for person 2

breaking_bad()