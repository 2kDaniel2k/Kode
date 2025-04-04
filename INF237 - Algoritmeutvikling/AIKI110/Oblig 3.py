import RPi.GPIO as GPIO
from time import sleep

led_pin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Hjelpefunksjoner for blinkene av henholdsvis karakterene og lokasjonen i synsfeltet
# Siden avslutningen på blinkene er forskjellig fra starten, har vi laget to funksjoner for hvert av dem
def blink_karakter():
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.3)

def blink_karakter2():
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(2)

def blink_lokasjon():
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.3)

def blink_lokasjon2():
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led_pin, GPIO.LOW)

# Startsignalet
def start():
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(3)
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(1)

# Blinkene for de ulike karakterene
def roede():
    blink_karakter2()

def von_bleu():
    blink_karakter()
    blink_karakter2()

def jello():
    blink_karakter()
    blink_karakter()
    blink_karakter2()

def gronnar():
    blink_karakter()
    blink_karakter()
    blink_karakter()
    blink_karakter2()

# Blinkene for de ulike lokasjonene i synsfeltet til agenten
def venstre():
    blink_lokasjon2()

def midten():
    blink_lokasjon()
    blink_lokasjon2()

def hoyre():
    blink_lokasjon()
    blink_lokasjon()
    blink_lokasjon2()

# Hovedfunksjonen som tar imot data fra kanalen og sender signaler til LED-lampen
# Første bokstaven i strengen er karakteren, og den andre er lokasjonen i synsfeltet
def blink(data):
    if data:    # Dersom meldingen fra kanalen ikke er tom - Det sendes kun melding når en karakter er i synsfeltet, ellers sendes ingen melding
        start()
        if data == "RV":
            roede()
            venstre()
        elif data == "RM":
            roede()
            midten()
        elif data == "RH":
            roede()
            hoyre()
        elif data == "VV":
            von_bleu()
            venstre()
        elif data == "VM":
            von_bleu()
            midten()
        elif data == "VH":
            von_bleu()
            hoyre()
        elif data == "JV":
            jello()
            venstre()
        elif data == "JM":
            jello()
            midten()
        elif data == "JH":
            jello()
            hoyre()
        elif data == "GV":
            gronnar()
            venstre()
        elif data == "GM":
            gronnar()
            midten()
        elif data == "GH":
            gronnar()
            hoyre()

GPIO.cleanup()