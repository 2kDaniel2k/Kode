#   Oppgave 2
#a) Vi definerer først funksjonen med grader og skala som input, hvor sistnevnte er satt til celcius
#som standardverdi. Deretter, lager vi funksjoner for omgjøring. Vi bruker så boolean uttrykk til å
#sjekke om skala er "C", "F" eller om man skal ta i bruk standardverdien, for å til slutt returnere
#riktig konvertering

def temperaturKonvertering(grader, skala="C"):
    celcius_til_farenheit = grader*(9/5)+32
    farenheit_til_celcius = (grader-32)*(5/9)
    if skala == "C":
        return celcius_til_farenheit
    elif skala == "F":
        return farenheit_til_celcius
    else:
        return celcius_til_farenheit


#   Oppgave 3
#a) Vi lager funksjoner for alle handlinger. Her bruker vi global saldo for at saldoen skal oppdateres
#etter hver handling. For uttak, lager vi feilmelding dersom det ikke er tilstrekkelige mdiler på konto.

saldo = 500

#Funksjon for innskudd
def innskudd(innskuddsmengde):
    global saldo
    if innskuddsmengde >= 0:
        saldo += innskuddsmengde
        return saldo
    else:
        return "Innskuddsmengde må være positiv"

#Funksjon for uttak
def uttak(uttaksmengde):
    global saldo
    if saldo >= uttaksmengde:
        saldo -= uttaksmengde
        return saldo
    else:
        return "Uttak mislyktes, ikke tilstrekkelige midler - få deg en jobb"

#Funksjon for rente på gjeldende konto
def rentesats(nåværende_saldo):
    if nåværende_saldo <= 1000000:
        return 0.01
    else:
        return 0.02

#Renteoppgjør
def renteoppgjør(nåværende_saldo):
    global saldo
    rente = saldo*rentesats(saldo)
    saldo += rente
    return saldo

#b) Vi lager en UI ved bruk av input()-funksjonen. Deretter, refererer vi til handlingene laget i
#forrige deloppgave for å kjøre ønskede operasjoner. Bruker også global saldo i starten av funksjonen
#for at saldoen skal oppdateres etter ved handlking.

def velg():
    global saldo
    valg = float(input(
        "--------------------\n"
        "1 - vis saldoen\n"
        "2 - innskudd\n"
        "3 - uttak\n"
        "4 - renteoppgjør\n"
            "--------------------\n"
    "Velg handling: "
    ))
    if valg == 1:
        return saldo
    elif valg == 2:
        innskuddsbeløp = float(input("Beløp: "))
        saldo += innskuddsbeløp
        return saldo
    elif valg == 3:
        uttaksmengde = float(input("Beløp: "))
        return uttak(uttaksmengde)
    elif valg == 4:
        saldoen = input("Skriv inn saldo: ")
        return renteoppgjør(saldoen)
    else:
        print("Ugyldig handling. Velg handling 1-4")


#c) Legger til en femte handling som viser de tre siste endringene.

saldo = 500
liste []

def innskudd(innskuddsmengde):
    global saldo
    if innskuddsmengde >= 0:
        saldo += innskuddsmengde
        return saldo
    else:
        return "Innskuddsmengde må være positiv"

def uttak(uttaksmengde):
    global saldo
    if saldo >= uttaksmengde:
        saldo -= uttaksmengde
        return saldo
    else:
        return "Uttak mislyktes, ikke tilstrekkelige midler - få deg en jobb"

def rentesats(nåværende_saldo):
    if nåværende_saldo <= 1000000:
        return 0.01
    else:
        return 0.02

def renteoppgjør(nåværende_saldo):
    global saldo
    rente = saldo*rentesats(saldo)
    saldo += rente
    return saldo

def velg():
    global saldo
    valg = float(input(
        "--------------------\n"
        "1 - vis saldoen\n"
        "2 - innskudd\n"
        "3 - uttak\n"
        "4 - renteoppgjør\n"
        "5 - siste endringer\n"
        "--------------------\n"
    "Velg handling: "
    ))
    if valg == 1:
        return saldo
    elif valg == 2:
        innskuddsbeløp = float(input("Beløp: "))
        saldo += innskuddsbeløp
        return saldo
    elif valg == 3:
        uttaksmengde = float(input("Beløp: "))
        return uttak(uttaksmengde)
    elif valg == 4:
        saldoen = input("Skriv inn saldo: ")
        return renteoppgjør(saldoen)
    elif valg == 5:
        input(
    else:
        print("Ugyldig handling. Velg handling 1-5")


        
