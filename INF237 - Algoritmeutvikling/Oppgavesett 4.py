# Nikola

import sys
import heapq

def nikola():
    data = list(map(int, sys.stdin.read().splitlines()))
    N = data[0]

    kostnad = [0] * (N + 1)   # Lager en tom liste (fylt med 0 som elementer) med kardinalitet N + 1
    for i in range(1, N + 1):   # Fyller listen med kostnadene for hver rute
        kostnad[i] = data[i]

    evig = 10**9    # Vi skal først fylle 2D-tabellen (N+1 x N+1) med umulig høye kostnader, for så å finne reelle kostnader som er billigere. Ruter med evig (stort tall) er ikke besøkt enda.

    tabell = [[evig] * (N + 1) for _ in range(N + 1)]    # 2D-tabellen representeres som en liste av lister. Hver rad er en rute (posisjon), mens kolonne er hopplengde brukt for å komme hit.
                                                        # Når vi finner et gyldig hopp, overskriver vi evig da dette vil være billigere enn evig.

    tabell[2][1] = kostnad[2]   # Første hopp er fast, som er fra rute 1 til 2, med hopplengde 1

    heap = []   # Lager en tom heap (prioriteringskø). I motsetning til en vanlig BFS-kø, vil heap sorteres med minste (billigste) øverst, dette vil redusere kjøretiden.
    heapq.heappush(heap, (kostnad[2], 2, 1))    # Legger til (akkumulert kostnad, posisjon, hopplengde)

    while heap:
        akkumulert_kostnad, posisjon, hopplengde = heapq.heappop(heap)  # Henter den billigste ruten først

        if akkumulert_kostnad > tabell[posisjon][hopplengde]:   # Dersom vi allerede har en billigere vei til denne posisjonen, hopper vi over og sparer kjøretid pga. unødvendige beregninger
            continue

        # Fremover hopp
        ny_hopplengde = hopplengde + 1
        ny_posisjon = posisjon + ny_hopplengde
        if ny_posisjon <= N:    # Sjekker at vi ikke hopper utenfor N
            ny_kostnad = akkumulert_kostnad + kostnad[ny_posisjon]
            if ny_kostnad < tabell[ny_posisjon][ny_hopplengde]:  # Sjekker om vi har funnet en billigere måte å komme til en spesifikk posisjon med spesifikk hopplengde.
                                                                                                # Som oftest overskriver dette bare evig, men det er mulig å overskrive posisjonen og hopplengden.
                tabell[ny_posisjon][ny_hopplengde] = akkumulert_kostnad + kostnad[ny_posisjon]    # Oppdaterer tabellen med den nye laveste kostnaden i denne posisjonen og hopplengden
                heapq.heappush(heap, (ny_kostnad, ny_posisjon, ny_hopplengde))  # Siden vi har funnet en ny billigere vei, lagrer vi den i køen (sortert) for å utforske videre på den seinere
        
        # Bakover hopp
        ny_posisjon = posisjon - hopplengde
        if ny_posisjon >= 1:  # Sjekk at vi ikke hopper før rute 1.
            ny_kostnad = akkumulert_kostnad + kostnad[ny_posisjon]
            if ny_kostnad < tabell[ny_posisjon][hopplengde]:
                tabell[ny_posisjon][hopplengde] = akkumulert_kostnad + kostnad[ny_posisjon]
                heapq.heappush(heap, (ny_kostnad, ny_posisjon, hopplengde))


    resultat = min(tabell[N])   # Indeks N i tabellen inneholder alle kostnadene for å nå denne ruten. De ulike elementene er de ulike hopplengdene.
    sys.stdout.write(str(resultat))

nikola()






# Spiderman's Workout

import sys

def spiderman():
    data = sys.stdin.read().splitlines()
    N = int(data[0])    # Antall test caser
    M = list(map(int, [data[i] for i in range(1, len(data), 2)])) # Antall distanser
    d = [list(map(int, data[i].split())) for i in range(2, len(data), 2)] # En liste av lister med distanser for test casene
    resultater = []

    for i in range(N):
        m = M[i]    # Antall distanser for caset vi ser på
        distanser = d[i] # Distansene for caset vi ser på
        tabell = [dict() for _ in range(m + 1)] # Lager  en liste med dictionaries for å holde styr på mulige kombinasjoenr. Nøkkelen er høyden vi er på etter x trekk, mens verdien består av et tuppel
                                                # som inneholder informasjon om hvordan vi kom dit (høyeste høyden vi har vært så langt, høyden vi var på før dette trekket, trekk (U eller D)).
                                                # Eks: Trekk 0: tabell[0] = { 0: (0, None, None) }, her er det bare et nøkkel-verdi par.
                                                #      Trekk 4: tabell[4] = { 80: (80, 60, 'U'), 40: (60, 20, 'U'), 40: (60, 40, 'D'), 0: (40, 20, 'D') }, her har vi 4 nøkkel-verdi par
        tabell[0][0] = (0, None, None)  # Første tilstand er 0 meter som høyeste nivå så langt, None høyde før dette og None trekk (U eller D) tidligere

        for j in range(m):
            d_verdi = distanser[j]  # Henter distansen Spiderman skal klatre dette trekket
            for h, (maks_h, _, _) in tabell[j].items(): # Går gjennom alle mulige høyder Spiderman kan være etter j trekk
                # Mulighet 1: Klatre opp (alltid mulig)
                ny_h = h + d_verdi    # Ny høyde øker i tilfellet hvor vi klatrer oppover
                ny_maks = ny_h if ny_h > maks_h else maks_h    # Oppdaterer makshøyden dersom ny_h er større enn tidligere makshøyde
                if ny_h not in tabell[j + 1] or tabell[j + 1][ny_h][0] > ny_maks:   # Siden vi vil ha oversikt over alle høyder Spiderman kan nå etter j + 1 trekk, sjekker vi to ting:
                                                                                   # 1. Hvis ny_h ikke finnes i tabellen, legger vi den til
                                                                                   # 2. Hvis ny_h allerede finnes, sjekker vi om vi kan komme dit med en lavere makshøyde (fordi vi vil ha lavest mulig
                                                                                   #    makshøyde). Altså lagrer vi dersom den nye makshøyden er lavere enn den som er lagret tidligere.
                                                                                   # tabell[j + 1] er hvilke høyder vi kan nå etter i neste trekk (+1), tabell[j + 1][ny_h][0] henter makshøyden så langt
                    tabell[j + 1][ny_h] = (ny_maks, h, "U")    # Vi lagrer den beste måten å nå ny_h etter j + 1 trekk. Altså (ny makshøyde, forige høyde, hvilke vei vi klatret (opp)
                        
                # Mulighet 2: Klatre ned (kun gyldig dersom vi ikke går under bakkenivå)
                if h >= d_verdi:
                    ny_h = h - d_verdi
                    ny_maks = maks_h    # Makshøyden endrer seg naturligvis ikke når vi klatrer
                    if ny_h not in tabell[j + 1] or tabell[j + 1][ny_h][0] > ny_maks:
                           tabell[j + 1][ny_h] = (ny_maks, h, "D")
        if 0 not in tabell[m]:  # Dersom vi ikke klarte å komme tilbake til bakkenivå etter m-trekk, er det umulig
            resultater.append("IMPOSSIBLE")
        else:
            trekk_sekvensen = []    # Denne vil bestå av "U" og "D"
            hoyde_no = 0    # Siden vi vet at vi kom oss tilbake på bakkenivå, skal vi spore tilbake hvordan vi kom hit
            for i in range(m, 0, -1):   # Vi starter på siste trekk, og går bakover ett trekk om gangen
                tilstand_no = tabell[i][hoyde_no]   # Høyden (nøkkelen) vi er på i det aktuelle trekket tilsvarer verdien i fortegnelsen, hvilket er et tuppel med informasjon om hvordan man kom seg dit
                trekk = tilstand_no[2]  # Vi henter indeks 2, altså tredje elementer i tuppelet, som er "U" eller "D"
                trekk_sekvensen.append(trekk)   # Legger trekket ("U" eller "D") til listen trekk_sekvensen
                hoyde_no = tilstand_no[1]   # Nå henter vi høyden i det aktuellet tuppelet for å fortsette å spore bakover i tabellen
            trekk_sekvensen.reverse()   # Siden vi bygde sekvensen baklengs må vi reversere
            resultater.append("".join(trekk_sekvensen))

    sys.stdout.write("\n".join(resultater))
                

spiderman()