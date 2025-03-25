# Hidden Camera

import sys
import math

# Vektoroperasjoner
def kryssprodukt(u, v):
    return u[0] * v[1] - u[1] * v[0]

def vektor_substraksjon(a, b):
    return (a[0] - b[0], a[1] - b[1])

# Beregning av polygonareal med shoelace-algoritmen
def polygonareal(polygon):  # Tar inn hjørnekoordinater (x, y) til et polygon
    areal = 0
    n = len(polygon)    # Antall hjørner i polygonet
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # i + 1 henter simpelt neste hjørne, og % n sørger for at vi går rundt til starten igjen når vi er ferdige
        areal += x1 * y2 - x2 * y1  # Shoeleace-navnet kommer av at det ser ut som skolisser som krysser hverandre dersom man tegner opp punktene
    return abs(areal) / 2

# Lager et nytt polygon ved å kutte ut delene utenfor kameraets synsfelt
def ny_polygon(polygon, kamera, x, sjekk): # Tar inn polygonet, kameraets posisjon, en bvektor (skillelinje,) og en funksjon som sjekker om et punkt er innenfor synsfeltet
    ny = []
    n = len(polygon)
    for i in range(n):
        no = polygon[i]    # Nåværende hjørne
        neste = polygon[(i + 1) % n]   # Neste hjørne
        no_innenfor = sjekk(no)    # Sjekker om nåværende hjørne er innenfor synsfeltet - Returnerer True eller False
        neste_innenfor = sjekk(neste)   # Sjekker om neste hjørne er innenfor synsfeltet - Returnerer True eller False
        if no_innenfor and neste_innenfor:  # Hvis begge hjørnene er innenfor synsfeltet (altså hele kanten), legg til hjørnet "neste" i det nye polygonet
            ny.append(neste)
        elif no_innenfor and not neste_innenfor:  # Hvis kanten starter innenfor, men går ut av synsfeltet, må vi finne skjæringspunktet der kanten krysser "klippelinjen"
            A = vektor_substraksjon(no, kamera)   # Vektor fra kamera til nåværende hjørne
            B = vektor_substraksjon(neste, kamera)   # Vektor fra kamera til neste hjørne
            nevner = kryssprodukt(x, (B[0] - A[0], B[1] - A[1]))   # Kryssproduktet mellom retningsvektoren og vektoren mellom de to hjørnene
            if abs(nevner) < 1e-9:  # Hvis nevneren er (tilnærmet) 0, er vektorene parallelle og vi kan hoppe over denne kanten
                continue
            j = -kryssprodukt(x, A) / nevner   # t forteller oss hvor langt langs kanten skjæringspunktet ligger
            s_punkt = (no[0] + j * (neste[0] - no[0]), no[1] + j * (neste[1] - no[1]))   # Skjæringspunktet
            ny.append(s_punkt)   # Legg til skjæringspunktet i det nye polygonet
        elif not no_innenfor and neste_innenfor:  # Hvis kanten starter utenfor, men går inn i synsfeltet, må vi finne skjæringspunktet og legge til neste hjørnet
            A = vektor_substraksjon(no, kamera)   # Vektor fra kamera til nåværende hjørne
            B = vektor_substraksjon(neste, kamera)   # Vektor fra kamera til neste hjørne
            nevner = kryssprodukt(x, (B[0] - A[0], B[1] - A[1]))   # Kryssproduktet mellom retningsvektoren og vektoren mellom de to hjørnene
            if abs(nevner) < 1e-9:  # Hvis nevneren er (tilnærmet) 0, er vektorene parallelle og vi kan hoppe over denne kanten
                ny.append(neste)   # Legg til neste hjørne i det nye polygonet
            else:
                j = -kryssprodukt(x, A) / nevner
                s_punkt = (no[0] + j * (neste[0] - no[0]), no[1] + j * (neste[1] - no[1]))   # Skjæringspunktet
                ny.append(s_punkt)   # Legg til skjæringspunktet i det nye polygonet
                ny.append(neste)   # Legg til neste hjørne i det nye polygonet
    return ny  # Returnerer det nye polygonet

def main():
    data = sys.stdin.read().strip().split()
    cases = int(data[0])
    i = 1
    resultater = []

    for _ in range(cases):
        n = int(data[i])    # Antall hjørner i polygonet
        i += 1
        polygon = []
        for j in range(n):
            x = float(data[i])
            y = float(data[i + 1])
            i += 2
            polygon.append((x, y))  # Hjørnekoordinater
        total_areal = polygonareal(polygon)  # Beregner totalt areal av polygonet

        # Kameraet plasseres på den første veggen (midt mellom de to første hjørnene)
        punkt1 = polygon[0]  # Første hjørne
        punkt2 = polygon[1]  # Andre hjørne
        kamera = ((punkt1[0] + punkt2[0]) / 2, (punkt1[1] + punkt2[1]) / 2) # Kameraets posisjon er midtpunktet mellom de to første hjørnene

        # Beregner synsfeltet ved å beregne veggvektoren og normalen
        vegg = (punkt2[0] - punkt1[0], punkt2[1] - punkt1[1])  # Veggvektoren
        normal = (-vegg[1], vegg[0])  # Normalen til veggen er (-v_y, v_x) fordi polygonet går mot klokken (normalen peker innover)
        norm = math.sqrt(normal[0] ** 2 + normal[1] ** 2)  # Beregner lengden av normalen (norm)
        normalisert = (normal[0] / norm, normal[1] / norm)  # Normaliserer normalen (deler vektoren på sin egen lengde) ved å gjøre vektoren til en enhetsvektor (lengde = 1), uten å endre retningen

        # Synsfeltet er 90 grader med normalen som sentrum - må altså beregne 45 grader på hver side med normal som sentrum
        vinkel = math.pi / 4  # 45 grader i radianer
        cosA = math.cos(vinkel) # Cosinus og sinus til 45 grader trengs for å rotere vektoren
        sinA = math.sin(vinkel)

        # Definerer så to vektorer som er rotert 45 grader fra normalen og danner synsfeltet
        v1 = (normalisert[0] * cosA + normalisert[1] * sinA, -normalisert[0] * sinA + normalisert[1] * cosA)  # Vektor rotert 45 grader fra normalen
        v2 = (normalisert[0] * cosA - normalisert[1] * sinA, normalisert[0] * sinA + normalisert[1] * cosA)  # Vektor rotert -45 grader fra normalen

        # Definerer to funksjoner for å sjekke om et punkt er innenfor synsfeltet
        innenfor1 = lambda punkt: kryssprodukt(v1, (punkt[0] - kamera[0], punkt[1] - kamera[1])) >= -1e-9  # Sjekker om et punkt er innenfor synsfeltet v1 (venstre synsgrense)
        innenfor2 = lambda punkt: kryssprodukt(v2, (punkt[0] - kamera[0], punkt[1] - kamera[1])) <= 1e-9  # Sjekker om et punkt er innenfor synsfeltet v2 (høyre synsgrense)

        # Lager det nye polygonet med ny_polygon-funksjonen
        nytt_polygon = ny_polygon(polygon, kamera, v1, innenfor1)  # Først kuttes polygonet med v1
        nytt_polygon = ny_polygon(nytt_polygon, kamera, v2, innenfor2)  # Deretter kuttes det nye polygonet med v2

        # Beregner synlig areal, samt hvor mye dette utgjør av totalarealet
        synlig_areal = polygonareal(nytt_polygon)
        ratio = synlig_areal / total_areal

        resultater.append(f"{ratio:.6f}")

    sys.stdout.write("\n".join(resultater))

main()


# Pesky Mosquitoes

"""
For å sjekke hvor mange mygg vi kan fange med en opp-ned skål, sjekker vi alle mulige sirkler som kan fange mygg hvor to punkter ligger langs kanten.
Dette skaper to sirkler per mygg-par. Vi finner midtpunktet mellom to mygg, og finner to mulige sentre for sirkelen.
Vi beregner høyden fra midtpunktet til sirkelens sentrum, og finner enhetsnormalvektoren til linjen mellom myggene.
Vi itererer over de to mulige sirkel-sentrene og teller myggene som er innenfor eller på sirkelen.
"""

import sys
import math

def mosquitoes():
    data = sys.stdin.read().split()

    cases = int(data[0]) # Antall scenarioer
    i = 1
    resultater = []

    for _ in range(cases):
        m = int(data[i]) # Antall mygg
        d = float(data[i + 1]) # Diameteren til skålen
        i += 2

        r = d / 2.0 # Radius av skålen

        # Leser posisjonene til myggene og legger til i listen posisjoner
        posisjoner = []
        for _ in range(m):
            x = float(data[i])
            y = float(data[i + 1])
            i += 2
            posisjoner.append((x, y))
        
        mest = 0
        
        # Strategi 1: Sjekker hvor mange mygg som kan fanges i skålen med sentrum i hver mygg sin posisjon
        # Bruker Pythagoras i if-statement for å sjekke om myggen er innenfor skålen.
        # Avstand = sqrt((x - ax)^2 + (y - ay)^2), og sjekker om denne avstanden er mindre eller lik radiusen av skålen (kvadreres fordi vi må kvadrere avstand for å oppheve kvadratroten)
        # Legger til 1e-9 for å unngå avrundingsfeil
        for (ax, ay) in posisjoner:
            midten = sum(1 for (x, y) in posisjoner if (x - ax) ** 2 + (y - ay) ** 2 <= r ** 2 + 1e-9)
            mest = max(mest, midten)

        # Sjekker hvor mange mygg som kan fanges dersom to mygg er på kanten av skålen - Denne er mer effektiv men krever mer kjøretid
        for j in range(m):  # Mygg 1
            for k in range(j + 1, m): # Mygg 2
                x1, y1 = posisjoner[j]
                x2, y2 = posisjoner[k]
                dx = x2 - x1 # Avstanden mellom myggene
                dy = y2 - y1
                avstand = math.hypot(dx, dy) # Avstanden mellom myggene - Hypotenusen i en rettvinklet trekant
                if avstand > d: # Hvis avstanden er større enn diameteren til skålen, hopper vi over
                    continue
                # Midtpunktet mellom de to myggene beregnes ved å ta gjennomsnittet av x- og y-koordinatene
                midtpunkt_x = (x1 + x2) / 2.0
                midtpunkt_y = (y1 + y2) / 2.0

                # Høyden fra midtpunktet mellom to mygg opp til sirkelens sentrum
                # Bruker Pythagoras r^2 = (avstand / 2)^2 + h^2, h = sqrt(r^2 - (avstand / 2)^2)
                h = math.sqrt(r * r - (avstand / 2.0) ** 2)

                # Beregner enhetsnormalvektor (vinkelrett vektor med lengde 1) til linjen mellom myggene
                # Denne vektoren brukes til å flytte midtpunktet langs den vinkelrette normalen for å finne de to mulige sentrumene til en sirkel
                ux = -dy / avstand
                uy = dx / avstand

                sentrum1 = (midtpunkt_x + h * ux, midtpunkt_y + h * uy) # Første senter
                sentrum2 = (midtpunkt_x - h * ux, midtpunkt_y - h * uy) # Andre senter

                # Itererer over de to mulige sirkel-sentrene og teller myggene som er innenfor eller på sirkelen. Oppdatererj*n
                for (ax, ay) in [sentrum1, sentrum2]:
                    fanger = sum(1 for (x, y) in posisjoner if (x - ax) ** 2 + (y - ay) ** 2 <= r ** 2 + + 1e-9)
                    mest = max(mest, fanger)

        resultater.append(str(mest))

    sys.stdout.write("\n".join(resultater))

mosquitoes()