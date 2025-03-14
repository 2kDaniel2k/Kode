#Temainnlevering 5
# Oppgave 1
# Vi lager en funksjon som tar "tekst" som input. Vi oppretter så to variabler: (1)
# alle_vokaler og (2) antall_vokaler - som settes til null da dette er en tellevariabel.
# Deretter, lager vi en for-loop som går over hver bokstav i teksten, og dersom den
# oppdager at bokstaven finnes i alle_vokaler, vil den øke antall_vokaler med 1. Til slutt
# returneres det hele.

def antallVokaler(tekst):
    alle_vokaler = "aeiouyæøåAEIOUYÆØÅ"
    antall_vokaler = 0
    for bokstav in tekst:
        if bokstav in alle_vokaler:
            antall_vokaler += 1
    return f"Antall vokaler: {antall_vokaler}"
