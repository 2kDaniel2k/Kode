#   Emptying the Baltic

import sys
import heapq

def baltic():
    data = sys.stdin.read().splitlines()
    h, w = map(int, data[0].split())    # Høyden og bredden på koordinatsystemet
    i, j = map(int, data[-1].split())   # Plasseringen av pumpen
    # Antar utifra oppgavetekst at i-, j-koordinatene starter på 1. For å justere dette i forhold til Python som begynner på indeks 0, trekker vi fra 1.
    i -= 1
    j -= 1
    ruter = [list(map(int, data[k].split())) for k in range(1, h + 1)]  # En liste med lister hvor hver liste representerer en rad (i)

    start_vann = ruter[i][j]    # Pumpens altitude (ligger alltid undedr havnivå)
    queue = [(start_vann, i, j)]    # Prioriteringskø (heap), med pumpens plassering.
    besokt = [[False] * w for _ in range(h)]    #  Besøkte ruter
    besokt[i][j] = True
    nytt_vannivå = [rad[:] for rad in ruter]    # Lager en kopi av ruter fordi vannivåer i ulike ruter kan endre seg
    
    total_mengde = 0

    retninger = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    while queue:
        altitude, i, j = heapq.heappop(queue)  # Pop-er ruten med lavest vannivå fra prioriteringskøen
        if altitude < 0:
            total_mengde += abs(altitude)    # Siden ruter under havnivå er negative, ønsker vi absoluttverdien da outputet av drenert vann skal være et positivt heltall

        for rad_bevegelse, kolonne_bevegelse in retninger:  # Nå ønsker vi å utforske alle 8 naboruter
            ny_i = i + rad_bevegelse
            ny_j = j + kolonne_bevegelse
            if 0 <= ny_i < h and 0 <= ny_j < w and not besokt[ny_i][ny_j]:  # Raden og kolonnen må være innenfor rutenettet, og kan ikke være besøkt tidligere
                besokt[ny_i][ny_j] = True
                # Dersom naboruten har en lavere altitude enn altituden til den aktuelle ruten, hever vi den til altituden til den aktuelle ruten.
                # Dette skal simulere at vannet fyller lavere terreng. Mao. kan vi kun drenere en lik mengde til originalaltituden, dersom naboen har lavere altitude.
                if ruter[ny_i][ny_j] < altitude:
                    nytt_vannivå[ny_i][ny_j] = altitude
                # Dersom naboruten har en lik eller høyere altitude, drenerer vi hele naboruten
                else:
                    nytt_vannivå[ny_i][ny_j] = ruter[ny_i][ny_j]
                ny_altitude = nytt_vannivå[ny_i][ny_j]
                heapq.heappush(queue, (ny_altitude, ny_i, ny_j))   # Legger til den oppdaterte naboruten i prioriteringskøen. Prioriteringskøen sørger for laveste nivå behandles først.

    print(total_mengde)

baltic()



#   Nature Reserve
import sys
import heapq

def nature():
    data = sys.stdin.read().splitlines()
    it = iter(data)    # Lager en iterator over listen data for å gå over hver linje med next
    d = int(next(it))   # Antall datasett
    output = []    # Oppretter en tom liste for å samle output-strenger for hvert datasett slik at de til slutt kan skrives ut samlet
    for _ in range(d):    # Itererer over hvert datasett
        N, M, L, S = map(int, next(it).split())    # N = Antall stasjoner, M = Antall kommunikasjonskanaler, L = Størrelse på programmet i bytes, S = Antall initielle stasjoner
        
        stasjoner = [int(x) - 1 for x in next(it).split()]    # Initielle stasjoner
        
        graf = [[] for _ in range(N)]    # Oppretter en liste med N tomme lister. Hver indre liste skal representere nabostasjonene (og tilhørende aktiveringskostnad) for en gitt stasjon
        for _ in range(M):    # Itererer over alle kommunikasjonskanalene hvor hver linje splittes i tre heltall (u startstasjon, v målstasjon, w vekt (aktivere kanalen))
            u, v, w = map(int, next(it).split())
            u -= 1     # 0-indeksere
            v -= 1
            graf[u].append((v, w))    # Legger til en kant i begge retninger (fordi kanalen er toveis) i graf
            graf[v].append((u, w))
        
        # Hvis alle stasjoner allerede har programmet, trengs ingen overføring
        if S == N:
            output.append("0")
            continue

        besokt = [False] * N    # Liste med N elementer over besøkte stasjoner
        queue = []    # Prioriteringskø
        i = 0    # Antall besøkte stasjoner
        total_aktivering = 0    # Akkumulerer den totale aktiveringskostnaden for kommunikasjonskanalene som blir brukt
        
        for s in stasjoner:    # Går gjennom alle initielle stasjoner
            if not besokt[s]:
                besokt[s] = True
                i += 1
                # Legger til alle kanaler (kanter) fra stasjonen s til naboene i prioriteringskøen, men kun for naboer som ikke er besøkt.
                # Hver kant legges inn som et par (w, v) der w er aktiveringskostnaden, slik at den billigste kanten alltid hentes ut først.
                for v, w in graf[s]:
                    if not besokt[v]:
                        heapq.heappush(queue, (w, v))
        
        while queue and i < N:  # Så lenge queue ikke er tom og ikke alle sjasjoner er besøkt
            w, u = heapq.heappop(queue)    # Henter ut kanten med lavest kostnad fra køen (w, u) der w er kostnaden og u er stasjonsindeksen
            if besokt[u]:    # Hvis stasjonen u allerede er besøkt, hopp over
                continue
            besokt[u] = True
            # # Hvis u ikke er besøkt, markeres den som besøkt, aktiveringskostnaden w legges til total_aktivering, og i økes
            # For den nye stasjonen u går vi gjennom alle naboene og legger til nye kanter i køen hvis naboene ikke er besøkt
            total_aktivering += w
            i += 1
            for v, w2 in graf[u]:
                if not besokt[v]:
                    heapq.heappush(queue, (w2, v))
        
        # total_aktivering er summen av aktiveringskostnadene for de brukte kanalene
        # L * (N - S) er energien brukt på overføring av programmet (L energi per overføring for hver stasjon som ikke allerede har programmet)
        total_energi = total_aktivering + L * (N - S) + 1
        output.append(str(total_energi))
        
    sys.stdout.write("\n".join(output))     # Etter at alle datasett er behandlet, skrives alle output-linjer ut, med hver linje separert av et linjeskift

nature()