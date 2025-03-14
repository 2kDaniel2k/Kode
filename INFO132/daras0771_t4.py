#               Temainnlevering 4
#   Oppgave 1
# Vi begynner med for-varianten. Her defineres først funksjonen, med tall som input. Deretter,
# lager vi en variabel kalt produkt, og setter til 1, som skal bli brukt til å akkumulere svaret.
# Det kommer så en for-loop som itererer i fra 1 til det valgte tallet i funksjonen (+1 fordi
# Python ikke leser til og med siste tallet). Her vil produktet vårt som starter på 1, multipliseres
# med i i range, og til slutt returnere produktet - hvilket er fakultetet av tallet skrevet inn i
# funksjonen fakultet(tall).

def fakultet(tall):
    produkt = 1
    for i in range(1, tall+1):
        produkt = produkt * i
    return produkt

# Lager tilsvarende funksjon for while-tilnærmingen. Hovedforskjellen ligger i at vi her også må
# introdusere en tellevariabel for å håndtere itereringen av funksjonen.

def fakultet1(tall):
    telleVariabel = 1
    akkumulator = 1
    while telleVariabel <= tall:
        akkumulator = akkumulator * telleVariabel
        telleVariabel += 1
    return akkumulator

#   Oppgave 2
# a) Vi lager en klasse kalt Monark og setter attributene til None. Deretter, bruker vi __init__
# til å initialisere attributene i klassen. Følgelig, lager vi en funksjonen skriv() som skal
# printe ut hver monark på en standardisert form. Vi definerer så Kongene, og til slutt lager vi en
# for loop som skal printe ut alle monarkene samlet.

class Monark():
    navn = None
    nasjon = None
    tiltredelsesår = None

    def __init__(self, navn, nasjon, tiltredelsesår):
        self.navn = navn
        self.nasjon = nasjon
        self.tiltredelsesår = tiltredelsesår

    def skriv(self):
        print(f"{self.navn} av {self.nasjon}, tiltrådt: {self.tiltredelsesår}")
        
haakon = Monark("Haakon VII", "Norge", 1905)
olav = Monark("Olav V", "Norge", 1957)
harald = Monark("Harald V", "Norge", 1991)

kongerekke = [haakon, olav, harald]

for Monark in kongerekke:
    Monark.skriv()

# b) 
