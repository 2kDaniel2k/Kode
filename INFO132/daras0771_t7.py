#           Innlevering 7
# Oppgave 1
# a) Vi legger inn listen venner fra oppgaveteksten. Deretter, lager vi en funksjon
# finnTelefon, som tar navn og venner (listen) som input. Vi itererer så over hver
# person i listen med en for-løkke. Så bruker vi if-statement til å sjekke om første
# elementet i hvert listeobjekt er likt navnet som ble brukt som input i funksjonen.
# Dersom dette stemmer overens, returneres det andre elementet i listeobjektet, som er
# telefonnummeret. Else "Ukjent person".

venner=[['Ole',99887766],['Liv',99778899],['Gro',99556644],
 ['Tom',98675601],['Eva',98987665],['Jan',88997766]]

def finnTelefon(navn, venner):
    for person in venner:
        if person[0] == navn:
            return person[1]
    else:
        return "Ukjent person"

# b) Vi oppretter funksjonen fjernTelefon som tar navn og liste som input. Deretter,
# lager vi en for-løkke som itererer over hvert objekt i listen. Vha. en if-statement
# sjekker vi om den første indeksen (navnet) i objektet tilsvarer input-navnet. Dersom
# dette stemmer, fjernes denne personen fra listen vha. liste.remove(person) og vi
# returnerer en liten melding. Dersom personen ikke finnes i listen, returneres en
# feilmelding.

def fjernTelefon(navn, liste):
    for person in liste:
        if person[0] == navn:
            liste.remove(person)
            return f"{navn} fjernet fra listen"
    else:
        return f"{navn} finnes ikke"

# Oppgave 2
# a)

Eksamen ={'INFO100':'C', 'INFO104':'B', 'INFO116':'E',\
 'INFO180':'A', 'INFO201':'F','INFO280':'C',\
 'GEO101':'D', 'GEO110':'B','ADM101':'A',\
 'ECON100':'B', 'ECON201':'C','GEO210':'C',\
 'FAIL101':'F'}

def kf(eksamen):
    A = 0
    B = 0
    C = 0
    D = 0
    F = 0
