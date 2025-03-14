# Turbo

"""
1. bygg --> Bygger et segmenttre for en gitt array:
   - m er nærmeste potens av 2 >= n
   - Bladnoder lagres på indeks m til 2m - 1
   - Interne noder lagrer summer av sine barn
2. query --> Henter sum i intervall [1, r):
    - Brukes for å telle aktive og fikserte posisjoner
3. oppdater --> Oppdaterer en verdi i segmenttreet:
    - Oppdaterer en enkelt indeks i tre til verdi
    - Justerer alle foreldrenoder for å opprethholde riktig sum
4. main --> Hovedfunksjonen som utfører Turbosort
    - Bygger to segmenttrær med bygg, tre_posisjon for å spore aktive posisjoner (1 = aktiv, 0 = inaktiv), og tre_verdi sporer fikserte tall (0 = ikke fiksert, 1 = fiksert).
      Aktive tall er tall som enda ikke er flyttet bort fra sin opprinnelige posisjon, mens ikke-fikserte tall er tall som enda ikke har blitt plassert på sin endelige plass
    - Bruker N faser for å sortere arrayet. Istedenfor å for sortere alle tallene en etter en i rekkefølge, plasserer vi de minste og største tallene vekselvis. Dette reduserer operasjoner siden vi bygger
      opp sorteringen fra begge sider samtidig
    - Beregner nåværende rangering og forventet plassering
    - Teller antall endringer som trengs
    - Oppdaterer tre posisjon ved å deaktivere posisjonen, og tre_verdi markeres som fiksert
"""

import sys

# Bygger segmenttre - Vi trenger både m og n fordi et segmenttre må være balansert (potens av 2), derfor har vi m i tillegg til n.
def bygg(array):
    n = len(array)    # Antall bladnoder (nederste nodene i treet) i array
    m = 1    # Representerer bladnoder (nederste nodene i treet) i segmenttreet. Vi ønsker å bygge det med den minste potensen av 2 som er større eller 1ik n
    while m < n:    # Så lenge m er mindre enn n, dobles verdien av m
        m *= 2
    # Hele segmenttreet trenger 2 * m plasser for både bladnoder (nederste nodene i treet) og interne noder (noder med barn)
    # Bladnodene ligger i indeksene m til 2 * m - 1
    # Interne noder ligger i indeksene 1 til m - 1
    # Roten av treet ligger i indeks 1
    tre = [0] * (2 * m)

    # Fyller inn de faktiske verdiene fra arrayet inn i bladnodene
    for i in range(n):
        tre[m + i] = array[i]    # Begynner på indeks m fordi bladnodene starter her. F.eks. tre[m] = array[0], tre[m+1] = array[1], tre[m+2] = array[2] osv.

    # Fyller inn interne noder (fra bunn til topp)
    for i in range(m - 1, 0, -1):
        tre[i] = tre[2 * i] + tre [2 * i + 1]   # Venstre barn + høyre barn
    return tre, m    # returnerer det ferdige segmenttreet samt äntall bladnoder

# Beregner elementene i intervallet [l, r), altså fra og med l og til men ikke med r. l og r er spørreintervallet.
def query(tre, m, l, r):
    summen = 0    # Holder summen fra l til r
    l += m; r += m  # Konverterer l og r fra 0-basert indeks til segmenttreets struktur - fordi bladnodene i segmenttreet starter på indeks m
    # Sjekker kun høyre barn fordi venstre barn automatisk er med - dette kommer av at når vi går oppover i segmenttreet, vil venstre barn bli inkludert uten spesielle sjekker.
    while l < r:    # Så lenge l er mindre enn r, betyr det at vi fortsatt har flere noder å besøke. Stopper når l == r fordi r er eksludert fra spørreintervallet [l, r).
                    # Partall er venstre barn og odetall er høyre barn i segmenttreet fordi roten er 1, venstre barn blir 2, høyre barn blir 3 osv.
        if l & 1:   # Sjekker om l er et oddetall (dvs. et høyre barn i segmenttreet). I så fall, reduser r med 1, og legg til tre[r] til summen fordi vi trenger denne verdien.
            summen += tre[l]
            l += 1
        if r & 1:   # Dersom r er et høyre barn, reduser med 1 og legg til tre[r] til summen. Reduserer fordi r er ekskludert fra spørreintervallet.
            r -= 1
            summen += tre[r]
        l //= 2; r //= 2    # Flytter l og r opp til foreldrenivået i segmenttreet
    return summen

# Oppdaterer en verdi i segmenttreet og justerer interne noder for å sikre at treet fortsatt inneholder riktige summer
def oppdater(tre, m, indeks, verdi):
    indeks += m    # Indeks begynner på m pga. bladnodene starter her
    tre[indeks] = verdi    # Setter ny verdi på bladnoden
    indeks //= 2    # Flytter indeks til foreldrenoden
    while indeks:    # Oppdaterer foreldrenoden rekursivt. Foreldrenoden er summen av sine to barn, og vi fortsetter opp hele veien til roten (indeks 1)
        tre[indeks] = tre[2 * indeks] + tre[2 * indeks + 1]
        indeks //= 2

def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0])    # n heltall
    heltall = [int(i) for i in data[1:n+1]]  # Liste med heltallene

    # Vi lagrer den opprinnelige posisjonen til hvert heltall i en liste. Bruker 1-indeksering.
    posisjon = [0] * (n + 1)
    for i, a in enumerate(heltall, start = 1):
           posisjon[a] = i 

    # Bygger to segmenttrær som holder styr på henholdsvis: (1) posisjoner som enda ikke er sortert, og (2) heltall som er plassert i sin endelige posisjon. Bruker bygg()-funksjonen vi lagde til dette.
    tre_posisjon, m1 = bygg([1] * n)
    tre_verdi, m2 = bygg([0] * n)        

    venstre, hoyre = 1, n    # venstre peker på neste minste tall i arrayet som enda ikke er sortert, hoyre peker tilsvarende største tallet. Ved å sortere fra begge ender kontra starte på ene enden
                             # sparer vi oss for operasjoner noe som gjør algoritmen mer effektiv.
    sorteringer = []    # Holder styr på antall sorteringer i hver fase - Dette blir outputet vårt til slutt
    for fase in range(1, n + 1):
        if fase % 2 == 1:    # Vi sorterer i oddetalls- og partallsfaser. Oddetallsfaser sorterer det neste minste tallet som enda ikke er fiksert, og partall for største
            x = venstre
            venstre += 1
        else:
            x = hoyre
            hoyre -= 1

        posisjon_x = posisjon[x] - 1    # Konverterer 1-indeksert posisjon til 0-indeksert
        rangering = query(tre_posisjon, m1, 0, posisjon_x + 1)    # Hvor mange tall det er før x i arrayet som fortsatt ikke er fiksert
        fiksert = query(tre_verdi, m2, 0, x - 1) if x > 1 else 0    # Hvor mange tall det er før x i arrayet som er fiksert
        ny_posisjon = x - fiksert    # Etter å fjerne de fikserte tallene, skal x være på x - fiksert
                                     # Eks: Hvis x = 3 og 1 er fiksert, blir ny_posisjon 3 - 1 = 2. x = 3 skal ligge på indeks 2 etter å ha fjernet de fikserte tallene.
        endringer = abs(rangering - ny_posisjon)    # Hvor mange posisjoner x må flyttes fra rangering til ny_posisjon
        sorteringer.append(str(endringer))    # Lagrer antall sorteringer for denne fasen
        oppdater(tre_posisjon, m1, posisjon_x, 0)    # Setter tre_posisjon[posisjon_x] = 0 for å markere at x ikke lenger er aktiv
        oppdater(tre_verdi, m2, x - 1, 1)   #    tre_verdi[x-1] = 1 for å markere x som fiksert --> Dette lar oss telle hvor mange tall mindre enn x som allerede er fiksert

    sys.stdout.write("\n".join(sorteringer))

main()



# Modulo Data Structures

"""
2 Operasjoner
    1. Øk alle tall i arrayet med indeks k med C, for alle indeks k hvor A(mod B). A(mod B) betyr at vi får resten A ved å dele et tall på B.
       F.eks. er 1(mod 2) alle oddetall fordi alle oddetall får rest = 1 når de deles på 2.

    2. Hent ut elementet array[D]

I tilfeller hvor mange tall blir påvirket (B er liten så mange tall som deles på B vil få rest A), vil vi unngå å iterere over hele arrayet og endre alle alle array[k].
Istedenfor, lager vi en liste bestående av en delmengde f.eks.: delmengde = [None, [0], [0, 0], [0, 0, 0]],
hvor hver indre liste i listen representerer en restklasse (gruppe av tall som gir samme rest) for en bestemt B.
delmengde[B] er en liste med B elementer, mens delmengde[B][A] lagrer summen av alle oppdateringer for tall k som oppfyller k % B == A.

F.eks.:
delmengde[1] har en plass [0] fordi alle tall har k % 1 == 0
delmengde[2] har en plass [0, 0] fordi tall kan ha k % 2 == 0 eller k % 2 == 1
delmengde[3] har en plass [0, 0, 0] fordi tall kan ha k % 3 == 0, k % 3 == 1 eller k % 3 == 2

Når vi gjør en oppdatering 1 A B C, legger vi til C i delmengde[B][A] istedenfor å oppdatere array[k] direkte.
Seinere, når vi skal utføre operasjon 2 D, henter vi simpelpt summen av relevvante mod[B][D % B] verdier for å beregne array[D].
"""

import sys
import math

def modulo():
    data = sys.stdin.read().splitlines()
    N, Q = map(int, data[0].split())    # N = lengden på arrayet, Q = antall queries 
    threshold = int(math.sqrt(N)) + 1    # Istedenfor å gjøre operasjoner på hele arrayet, bryter vi ned i blokker på kvadratroten av N + 1. O(N) --> O(sqrt(N)) per operasjon

    array = [0] * (N + 1)   # Lager en liste med N + 1 elementer satt til 0. Har +1 for 1-basert indeksering, hvor første elementet er 0, som ikke brukes.

    delmengde = [None] * threshold    # Lager en delmengde av array som er threshold-delmengden satt til None (skal fylles seinere)

    # Bygger en liste for hver verdi i, hvor lengden er i, alle satt till 0. Her skal restene når vi deler på B lagres.
    # Listen ser f.eks. slik ut: [
    #                               None,
    #                               [0],
    #                               [0, 0],
    #                               [0, 0, 0]
    #                            ]
    for i in range(1, threshold):
        delmengde[i] = [0] * i
    
    resultater = []

    for i in range(1, Q + 1):
        linjer = data[i].split()    # Splitter simpelt hver linje i input til en liste av tallene (som strenger)
        if linjer[0] == "1":    # Dersom første tallet i en inputlinje er 1, kjøres operasjon 1. A = restklassen for mod B, C = hvor mye som skal legges til
            A, B, C = int(linjer[1]), int(linjer[2]), int(linjer[3])
            # Dersom B (modulus) er liten vil antall påvirkede elementer være stort fordi mange k kan deles på et lite tall og få samme rest
            # Siden mange elementer må oppdateres, bruker vi tabellen delmengde istedenfor å gå over hele arrayet.
            if B < threshold:
                delmengde[B][A] += C
            else:
            # Dersom B er stor vil færre elementer bli påvirket, og vi itererer over arrayet direkte fordi det krever lite tid  
                start = A if A != 0 else B
                for k in range(start, N + 1, B):
                    array[k] += C
        else:
            D = int(linjer[1])   # D er knyttet til operasjon nummer 2, hvor vi simpelt skal hente ut elementet i arrayet med indeks D
            resultat = array[D] # resultat er grunnverdien til array[D], den starter som 0, men kan også bli endret direkte (dersom B er stor slik forklart ovenfor)
            for i in range(1, threshold):   # Vi legger til endringene som har blitt gjort når B har vært liten og vi ikke direkte endret arrayet. Mao. legger vi til alle tilfeller av operasjon 1.
                resultat += delmengde[i][D % i]
            resultater.append(str(resultat))
    sys.stdout.write("\n".join(resultater))

modulo()