# Errands

"""
Bruker minimal spanning tree (MST) for å finne den beste rekkefølgen for å besøke ærendene mellom work og home med minimal kjøretid.
MST finner det mest optimale spanning-treet mellom noder ved hjelp av Prim-algoritmen som tar i betraktning kantenes vekt, som i vår oppgave er avstanden.
Koden bruker en rekursiv søkealgoritme for å prøve ulike rekkefølger av ærender, men forkaster dårlige alternativer tidlig.
For hver delrute (ruten så langt) beregnes et optimistisk anslag på den totale kjørelengden ved å:
- Ta med faktisk kjørelengde så langt
- Legge til korteste avstand til et ubesøkt ærend
- Legge til MST over de gjenværende ærendene (uavhengig av rekkefølge)
- Legge til korteste avstand fra et ubesøkt ærend til home


Tester først noder med kortest avstand fra nåværende sted, og deretter de med lengre avstand (sortert liste nedenfor).
"""

import sys
import math

# Hjelpefunksjon som beregner avstand mellom to punkter (x, y)
def avstand(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Hjelpefunksjon for minimal spanning tree (MST).
# noder er en liste (eller et set) med stedsnavn, mens lokasjoner er en fortegnelse som kartlegger stedsnavn til (x, y)-koordinater.
def mst(noder, lokasjoner):
    gjenverende = set(noder)    # Kopi av listen over noder. Gjør til sett fordi det er raskere å fjerne noder slik (skjer i O(1) tid).
    noverende = gjenverende.pop()    # Start med et vilkårlig element
    total = 0.0    # Denne variabelen bil holde summen av vektene til kantene vi legger til i MST-en
    i_treet = {noverende}    # Lager et sett med noder som vi allerede har tatt med i MST-en (starter med den første noden vi valgte)
    
    # I hver iterasjon finner vi den korteste kanten fra en allerede besøkt node i i_treet til en ubesøkt node i gjenverende.
    # Legger så denne korteste kanten til den totale vekten, og oppdaterer hvilke noder som er inkludert i MST-en.
    # Til slutt returneres den totale vekten for MST-en
    while gjenverende:
        beste = float('inf')
        beste_node = None
        for u in i_treet:
            for v in gjenverende:
                distanse = avstand(lokasjoner[u], lokasjoner[v])
                if distanse < beste:
                    beste = distanse
                    beste_node = v
        total += beste
        i_treet.add(beste_node)
        gjenverende.remove(beste_node)
    return total

# Finner optimal løsning for den aktuelle dagen. Utforsker de ulike rekkefølgene, men 
# Returnerer den beste rekkefølge som en liste med stedsnavn
def los_dag(lokasjon, errands):
    beste_distanse = float('inf')
    beste_sti = None

    # noverende = stedet vi befinner oss på nå, ubesokt = sett med ubesøkte ærender, total_distanse = total distanse så langt i denne ruten,
    # rekkefolge = rekkefølgen vi har besøkt ærendene i til nå
    def finn(noverende, ubesokt, total_distanse, rekkefolge):
        nonlocal beste_distanse, beste_sti
        # Hvis alle ærender er besøkt, legg til avstanden til home
        if not ubesokt:
            total = total_distanse + avstand(lokasjon[noverende], lokasjon["home"])
            if total < beste_distanse:
                beste_distanse = total
                beste_sti = rekkefolge[:]
            return

        # Beregner lower bound:
        # 1) En estimert billigste kostnad for å nå neste ubesøkte sted
        # 2) En estimert billigste kostnad for å komme hjem fra det neste ubesøkte stedet
        # 3) En estimert billigste kostnad for å besøke alle gjenværende ubesøkte steder (MST)

        # Beregner den korteste mulige avstanden fra det stedet vi er på nå til et av de ubesøkte ærendene - Dette er den minst kostbare neste bevegelsen
        minste_fra_noverende = min(avstand(lokasjon[noverende], lokasjon[u]) for u in ubesokt)

        # Beregner korteste mulige avstanden fra en vilkårlig ubesøkt ærende til home - Dette representerer den billigste veien hjem
        minste_veien_hjem = min(avstand(lokasjon[u], lokasjon["home"]) for u in ubesokt)
    
        # Beregner den minimale totale kostnaden for å koble sammen de gjenværende ærendene, med MST
        # Gir optimistisk vurdering av ruten gjennom ærendene (uten å tenke på rekkefølge)
        mst_kostnad = mst(ubesokt, lokasjon)
    
        # "Selv om jeg gjør alt perfekt herfra, kan jeg ikke gjøre det billigere enn dette"
        # Dersom nåværende rute allerede er verre enn den beste vi har funnet så langt, beskjær denne grenen istedenfor å gå dypere i treet
        lower_bound = total_distanse + minste_fra_noverende + mst_kostnad + minste_veien_hjem
        if lower_bound >= beste_distanse:
            return

        # Bæskjering er mer effektiv dersom vi prøver de ubesøkte ærendene i stigende rekkefølge av avstand fra nåværende sted
        for u in sorted(ubesokt, key=lambda x: avstand(lokasjon[noverende], lokasjon[x])):
            d = avstand(lokasjon[noverende], lokasjon[u])   # Avstand fra nåværende sted til ærend u
            ny_d = total_distanse + d    # Ny total kjørelengde hvis vi velger å dra dit nå
            if ny_d >= beste_distanse:  # Hvis den nye totalen allerede er større enn den beste vi har funnet, beskjær denne grenen
                continue
            # Oppdaterer så hva som er ubesøkt, og går rekursivt videre med u som neste steg, og legger det til i ruten (rekkefolge)
            ny_ubesokt = ubesokt.copy()
            ny_ubesokt.remove(u)
            finn(u, ny_ubesokt, ny_d, rekkefolge + [u])

    # Start rekursjonen fra "work" med alle ærender ubesøkt
    finn("work", set(errands), 0.0, [])
    return beste_sti

def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0].strip())    # n er antall lokasjoner
    lokasjoner = {}    # Fortegnelse som holder styr på navn (nøkkel) og koordinater (verdi) til hver lokasjon
    for i in range(1, n + 1):
        linje = data[i].split()    # Hver linje består av navn x-koordinat y-koordinat
        navn = linje[0]
        x = float(linje[1])
        y = float(linje[2])
        lokasjoner[navn] = (x, y)
    
    # Resten av linjene i inputen beskriver ærendene for hver dag
    for linje2 in data[n + 1 : ]:

        errands = linje2.split()
        beste_rekkefolge = los_dag(lokasjoner, errands)
        # Skriv ut rekkefølgen for ærendene (uten "work" eller "home")
        print(" ".join(beste_rekkefolge))

main()


# Bus Planning

"""
Målet er å dele en klasse med elever i færrest mulig grupper slik at:
    - Ingen fiender havner i samme gruppe
    - Gruppestørrelsen ikke overskrider bussens kapasitet (c)
Løses med rekursiv dynamisk programmering og memoization.

Bruker memoization fordi det utforskes mange ulike gruppekombinasjoner rekursivt, og:
(1) samme delproblem (sett med gjenværende elever som må allokeres) kan oppstå flere ganger via forskjellige veier
(2) hvis vi allerede har funnet den optimale løsningen for et bestemt sett med elever, så kan vi gjenbruke den direkte
Derfor lagrer vi tidligere resultater for å redusere kjøretiden.

Oversikt over funksjoner:

    mulige_grupper(gjenverende_elever):
- Genererer alle gyldige grupper fra en gitt mengde elever.
- En gyldig gruppe har maks c elever og inneholder ingen fiender.
- Gruppen må inkludere den minste indeksen i inputmengden for å unngå duplikater.

    resultat(gjenverende):
- Bruker dynamisk programmering for å finne en optimal gruppering (minst mulig antall grupper).
- Kaller mulige_grupper for å finne gyldige førstegupper, og løser deretter delproblemet rekursivt på de resterende elevene.
  Dvs. vi antar at vi starter løsningen med en av de gyldige gruppene. F.eks. gjenverende = {0,1,2} og c = 2, så kan vi velge å starte med gruppen [0,2].
  Når vi har valgt én gruppe, fjerner vi disse elevene fra remaining, og gjentar hele prosessen (resultat(...)) på de elevene som er igjen (delproblemet).
  Eksempel: Etter å ha plassert [0,2] i en gruppe, gjenstår {1}. Da kaller vi resultat(frozenset({1})).
- Bruker memoization (fortegnelse) for å huske tidligere løsninger og unngå unødvendig rekursjon.

Programmet avsluttes med å kalle resultat på hele elevmengden, formatterer resultatet, og skriver ut:
    - Først antall grupper
    - Deretter én linje per gruppe med navnene til elevene
"""

import sys

def main():
    data = sys.stdin.read().split()

    iterator = iter(data)
    n = int(next(iterator)) # Antall elever
    k = int(next(iterator)) # Antall fiendeforhold
    c = int(next(iterator)) # Maks antall elever i en buss
    navn = [next(iterator) for _ in range(n)] # Leser de neste n elementene, som er navnene på elevene, og lagrer i listen navn
    
    # Tilordner hvert navn (nøkkel) et heltall (verdi) som representerer indeksen i listen vi lagde ovenfor - Dette lagres som en fortegnelse
    # Eks.: {
    # "Alice": 0,
    # "Bob": 1,
    # "Charlie": 2
    # }
    indeks = {}
    for i, navnet in enumerate(navn):
        indeks[navnet] = i
    
    # Lager en liste med sett for fiender til hver elev. F.eks. fiender[0] = {1, 3} betyr at elev 0 er fiende med elev 1 og 3.
    fiender = [set() for _ in range(n)] # Opretter en liste med n tomme sett
    # Leser de neste k parene med fiender og oppdaterer fiender-listen
    for _ in range(k):
        a = next(iterator)
        b = next(iterator)
        i = indeks[a]
        j = indeks[b]
        fiender[i].add(j)
        fiender[j].add(i)
    
    # Lager en fortegnelse for å lagre tidligere beregninger
    # Nøkkelen er et frozenset av indekser til elever som gjenstår å allokere. F.eks. ({0, 1, 3}) betyr --> Hva er den beste måten å allokere elevene 0, 1 og 3 på?
    # Verdien er et tuppel (minimum_antall_grupper, liste_av_grupper) hvor minimum_antall_grupper er det minste antallet grupper uten å danne fiender eller
    # overstige bussens kapasitet, mens liste_av_grupper er en liste av selve gruppefordelingen.
    # F.eks. betyr (2, [[0, 2], [1]]) --> Man trenger 2 grupper, hvor 0 og 2 er i den første gruppen og 1 er i den andre.

    fortegnelse = {}
    
    # Funksjon for å generere alle mulige grupper av elever som ikke danner fiender og som ikke overstiger kapasiteten c
    def mulige_grupper(gjenverende_elever):
        if not gjenverende_elever:
            return []
        sortert = sorted(gjenverende_elever)
        # Viktig detalj: Tar alltid med den første eleven i den sorterte listen over gjenværende elever for å unngå å lage samme grupper med ulike rekkefølger
        # F.eks. [2, 5] og [5, 2]
        alltid_forste = sortert[0]
        gyldige_grupper = []
        # Rekursiv funksjon for å lage grupper ved å legge til kandidater til den nåværende gruppen
        def rekursiv(noverende_gruppe, kandidater, start):
            # Legger til kopi av den nåværende (gyldige) gruppen til gyldige_grupper som er alle gyldige grupper du har funnet så langt
            # Vi må kopiere den nåværende gruppen fordi den kan endres videre i rekursjonen, og vi vil bevare den slik den er nå
            gyldige_grupper.append(list(noverende_gruppe))
            # Hvis gruppen allerede har maks antall elever, stopp videre utvidelse (append)
            if len(noverende_gruppe) == c:
                return
            # Itererer gjennom kandidatene, fra og med start-posisjonen.
            # start gjør at vi ikke vurderer tidligere indekser igjen, og dermed unngår duplikate grupper i ulik rekkefølge.
            for i in range(start, len(kandidater)):
                kandidat = kandidater[i]    # Kandidat til å bli med i den nåværende gruppen
                # Går gjennom alle som allerede er i gruppen (noverende_gruppe), og dersom kandidaten er fiende med noen av dem settes conflict = True
                konflikt = False
                for member in noverende_gruppe:
                    if kandidat in fiender[member]:
                        konflikt = True
                        break
                if konflikt:    # Dersom det er en konflikt, hopper vi over denne kandidaten og fortsetter til neste
                    continue
                noverende_gruppe.append(kandidat)   # Etter å ha sjekket at kandidaten passer med alle i gruppen, legger vi dem til
                                                    # Kaller rekursivt for å fortsette å legge til flere kandidater i den nåværende gruppen
                rekursiv(noverende_gruppe, kandidater, i + 1)     # Legger så inn neste kandidat i samme gruppe for å se om det går bra
                                                             # i + 1 fordi vi ikke vil ha med den samme kandidaten igjen i neste runde
                                                             # Vi bygger altså videre på denne gruppen med de resterende (i + 1) kandidatene rekursivt
                noverende_gruppe.pop()    # Etter at vi har prøvd ferdig alle utvidelser med denne kandidaten, fjerner vi den igjen
                                          # Dette er backtracking! Fordi vi går tilbake for å prøve andre muligheter uten denne kandidaten.
        # Henter alle kandidater utenom den minste indeksen, som vi alltid tvinger inn i gruppen først. Dette hindrer duplikater som [1,2] og [2,1].
        kandidater = sortert[1:]
        rekursiv([alltid_forste], kandidater, 0)    # Starter rekursjonen med en gruppe som kun inneholder first
                                               # Deretter forsøker vi å legge til flere elever fra candidates
        return gyldige_grupper

    # Beregner det minste antall grupper som trengs for å fordele de gjenværende elevene
    # Returnerer tuppeter (min_antall_grupper, liste_av_grupper)
    def resultat(gjenverende):
        if not gjenverende:    # Base case: Hvis det ikke er flere elever igjen å allokere, returner 0 grupper og en tom liste
            return (0, [])
        if gjenverende in fortegnelse:    # Dersom dette delproblemet allerede er løst, returner det lagrede resultatet
            return fortegnelse[gjenverende]
        
        beste_antall = float('inf')    # Holder styr på det minste antallet grupper vi har funnet så langt
        best_fordeling = None    # Holder styr på den tilhørende grupperingen (hvordan elevene ble fordelt i grupper)
        gyldige_grupper = mulige_grupper(gjenverende)    # Genererer alle gyldige grupper av gjenværende elever. Her er hver gruppe en liste med elev-indekser.
        for gruppe in gyldige_grupper:    # Itererer gjennom hver mulig gyldig gruppe for å se hvilken som gir minste antall grupper totalt
            ny_gjenverende = set(gjenverende) - set(gruppe)    # Fjerner gruppen fra de gjenværende elevene for å finne ut hvem som fortsatt må grupperes
            ny_gjenverende = frozenset(ny_gjenverende)    # Konverterer tilbake til frozenset, fordi resultat bruker frozenset som nøkkel i fortegnelsen
            antall, inndeling = resultat(ny_gjenverende)    # Kaller resultat rekursivt for å finne ut hvor mange grupper som trengs for de gjenværende elevene
                                                            # antall er antall grupper som trengs for å plassere ny_gjenverende
                                                            # inndeling er hvordan de ble gruppert
            totalt = 1 + antall    # Legger til 1 fordi vi bruker én ny gruppe nå, i tillegg til gruppene i den rekursive løsningen
            # Dersom denne løsningen er bedre enn den beste vi har funnet så langt, oppdaterer vi beste_antall og best_fordeling
            if totalt < beste_antall:
                beste_antall = totalt
                best_fordeling = [gruppe] + inndeling
        # Når vi har prøvd alle muligheter for gjenverende, lagrer vi den beste løsningen i fortegnelsen for å unngå å gjøre det samme igjen senere
        fortegnelse[gjenverende] = (beste_antall, best_fordeling)
        return fortegnelse[gjenverende]
    
    totalt_grupper, inndeling = resultat(frozenset(range(n)))   # Kaller resultat med alle elevene (0 til n-1) som gjenverende elever
    
    # Formater utskriften: Antall grupper, deretter en linje per gruppe med navn.
    output_linjer = []    # Lager en tom liste output_lines, som skal fylles med linjer som senere skrives ut
    output_linjer.append(str(totalt_grupper))    # Første linje i output er antall grupper
    for gruppe in inndeling:    # Itererer gjennom hver gruppe i inndeling (som er en liste med lister av elev-indekser)
        gruppe_navn = [navn[i] for i in gruppe]    # For hver gruppe (som består av elev-indekser), slår vi opp navnene fra navnelisten
                                                   # Resultatet er en liste gruppe_navn med navnene på elevene i den aktuelle gruppen
        output_linjer.append(" ".join(gruppe_navn))    # Gjør gruppe_navn om til én tekstlinje ved å slå sammen navnene med mellomrom. F.eks. ["Alice", "Bob"] --> "Alice Bob".
    
    print(totalt_grupper)
    for gruppe in inndeling:
        print(" ".join(navn[i] for i in gruppe))

main()