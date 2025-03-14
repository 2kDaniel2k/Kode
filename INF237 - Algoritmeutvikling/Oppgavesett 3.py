# Nested Dolls
import sys

def nested_dolls():
    data = sys.stdin.read().splitlines()
    antall_cases = int(data[0])
    antall_dukker = [int(data[i + 1]) for i in range(0, antall_cases * 2, 2)]
    # En liste av lister over dimensjoner til de ulike test-casene, lagret som tupler
    dimensjoner = [[(int(w), int(h)) for w , h in zip(data[i].split()[::2], data[i].split()[1::2])] for i in range(2, antall_cases * 2 + 1, 2)]
    # Sorterer bredde stigende, deretter høyde synkende (om bredden er lik). Sorterer høyde synkende slik at dukker ikke nestes dersom de har lik bredde, men neste dukke har høyere høyde.
    sorterte_dimensjoner = [sorted(case, key = lambda x: (x[0], -x[1])) for case in dimensjoner]

    resultater = []
    for case in sorterte_dimensjoner:
        # Piles består av ulike stacks av nested dolls, vi ønsker å minimere antall stacks. Hvert element lagrer høyeste høyden til stacken. 
        piles = []
        # Bruker binært søk for å finne riktig plassering for h i piles, slik at vi kan erstatte en eksisterende høyde eller starte en ny stack
        for _, h in case:
            v = -1 # v lagrer indeksen til den siste stacken i listen piles (toppverdien til høyeste dukke) som er mindre enn den nåværende dukkes høyde. Mao. er v stacken den den nåbærende
                   # dukkens høyde kan plasseres slik at den nestes inn i den forrige dukkens høyde.
            venstre = 0
            hoyre = len(piles) - 1
            while venstre <= hoyre:
                midten = (venstre + hoyre) // 2    # Finne midterste indeks
                if piles[midten] < h:   # Dersom nåværende høyde er mindre enn den midterste stacken i piles, gå til høyre
                    v = midten
                    venstre = midten + 1
                else:
                    hoyre = midten - 1   # Tilsvarende for å gå til venstre
            # Etter at det binære søket er over, bestemmes det hvor høyden til nåværende dukke skal plasseres i piles
            if v != -1:
                piles[v] = h
            else:
                piles.insert(0, h) # Hvis venstre er på slutten av piles, betyr det at h er den største høyden så langt. Vi må starte en ny stack fordi ingen eksisterende
                                   # stack kan inneholde h uten å bryte nesting-regelen.

        resultater.append(str(len(piles))) # Antall stacks i piles er minimum antall "dukke-samlinger" man kan lage

    sys.stdout.write("\n".join(resultater)) # Skriver ut svaret linje for linje

nested_dolls()



# Tree Shopping

import sys

def tree_shopping():
    data = sys.stdin.read().splitlines()
    n, k = map(int, data[0].split()) # n = antall trær, k = trær Andy må kjøpe
    a = list(map(int, data[1].split())) # Liste med høydene på trærne

    # For å legge til en verdi i starten av en liste, må alle elementer flyttes en til høyre, noe som tar O(n) tid. Ved å bruke deque's kan vi få det ned til O(1)
    maks_liste = []
    min_liste = []
    minste_forskjell = float("inf") # Setter forskjellen til en høy verdi (evig) fordi kun minste forskjeller under vil bli lagret i koden fremover

    for i in range(n):
        # Fjerner verdier som har gått ut av vinduet
        # maks_liste sjekker om listen ikke er tom, ellers får vi index error av maks_liste[0] om den er tom.
        # maks_liste[0] < i - k + 1 sjekker om første element er utenfor vinduet og må fjernes.
        if maks_liste and maks_liste[0] < i - k + 1:
            maks_liste.pop(0) # Dersom den nye indeksen i i maks_liste er større en den største verdien til nå (maks_liste[0]), så fjernes maks_liste[0] til fordel for den nye største veriden n
        if min_liste and min_liste[0] < i - k + 1:
        # Tilsvarende for minste verdier
            min_liste.pop(0)

        # Fjerner verdier som ikke lenger er relevante i maks_liste
        # Sjekker om a[i] er større enn de tidligere verdiene i maks_liste, og fjerner siste elementet i så fall. Dette sikrer at maks_liste alltid har den største verdien først.
        while maks_liste and a[maks_liste[-1]] <= a[i]:
                maks_liste.pop()
        maks_liste.append(i)
        # Tilsvarende for min_liste
        while min_liste and a[min_liste[-1]] >= a[i]:
                min_liste.pop()
        min_liste.append(i)
        # Beregner minste_forskjell når minst k elementer er samlet
        if i >= k - 1:
            minste_forskjell = min(minste_forskjell, a[maks_liste[0]] - a[min_liste[0]])

    print(minste_forskjell)

tree_shopping()