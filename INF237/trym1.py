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


