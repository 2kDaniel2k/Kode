


#   Emptying the Baltic

import sys

def baltic():
    data = sys.stdin.read().splitlines()
    h, w = map(int, data[0].split())    # Høyden og bredden på koordinatsystemet
    i, j = map(int, data[-1].split())   # Plasseringen av pumpen
    # Antar utifra oppgavetekst at i-, j-koordinatene starter på 1. For å justere dette i forhold til Python som begynner på indeks 0, trekker vi fra 1.
    i -= 1
    j -= 1
    ruter = [list(map(int, data[k].split())) for k in range(1, h + 1)]  # En liste med lister hvor hver liste representerer en rad (i)

    start_vann = ruter[i][j]
    besokt = [[False] * w for _ in range(h)]    #  Besøkte ruter
    queue = [(i, j)]
    besokt[i][j] = True

    total_mengde = 0

    while queue:
        i, j = queue.pop(0)  # FIFO
        rute_altitude = ruter [i][j]  # Henter vann mengden fra den aktuelle ruten
        if rute_altitude >= start_vann:   # Sjekker om altituden i den aktuelle ruten har høyere eller lik altitude som pumpens plassering - i så fall kan alt pumpes, gitt at det også er under havnivå
            pumpet_vann = abs(rute_altitude) if rute_altitude < 0 else 0    # Dersom altituden er under havnivå pumpes alt vannet i ruten
        else:
            pumpet_vann = abs(start_vann)    # Dersom altituden er lavere enn pumpen, kan vi maksimalt pumpe en mengde tilsvarende pumpens altitude
        total_mengde += pumpet_vann

        # Sjekker alle 8 naboceller, ved å lage alle mulige forflytninger
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                if a == 0 and b == 0:   # Unngår å besøke nåværende celle - Vil kunne sjekke naboene
                    continue
                ny_i, ny_j = a + i, b + j
                if 0 <= ny_i < h and 0 <= ny_j < w and not besokt[ny_i][ny_j]:  # Sjekker at nye posisjonen er innenfor rutenettet
                    besokt[ny_i][ny_j] = True
                    queue.append((ny_i, ny_j))

    print(total_mengde)

baltic()

