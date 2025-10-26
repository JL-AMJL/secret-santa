from copy import deepcopy
from itertools import permutations

# Vergleichsliste 1
liste1 = {
    'Jannes': ['Esther', 'Lea', 'Sébastien'],
    'Abdalla': ['Charlotte', 'Stephanie', 'Esther'],
    'Christian': ['Lea', 'Charlotte', 'Stephanie'],
    'Lea': ['Abdalla', 'Sébastien', 'Jannes'],
    'Esther': ['Christian', 'Abdalla', 'Charlotte'],
    'Charlotte': ['Sébastien', 'Jannes', 'Abdalla'],
    'Sébastien': ['Stephanie', 'Christian', 'Lea'],
    'Stephanie': ['Jannes', 'Esther', 'Christian']
}

# Vergleichsliste 2
liste2 = {
    'Jannes': ['Charlotte', 'Stephanie', 'Lea'],
    'Abdalla': ['Jannes', 'Sébastien', 'Esther'],
    'Christian': ['Stephanie', 'Esther', 'Sébastien'],
    'Lea': ['Esther', 'Abdalla', 'Christian'],
    'Esther': ['Lea', 'Charlotte', 'Jannes'],
    'Charlotte': ['Christian', 'Jannes', 'Stephanie'],
    'Sébastien': ['Abdalla', 'Lea', 'Charlotte'],
    'Stephanie': ['Sébastien', 'Christian', 'Abdalla']
}

vergleichslisten = [liste2]
namen = ['Jannes', 'Abdalla', 'Christian', 'Lea', 'Esther', 'Charlotte', 'Sébastien', 'Stephanie']
spalten_an = 3

lösungen = []

def ist_gueltig(aktuelle_liste, name, kandidaten, vergleichslisten, spalte_besetzungen):
    # Keine Dopplung in der Zeile
    if len(kandidaten) != len(set(kandidaten)):
        return False
    # Zeilenname darf nicht vorkommen
    if name in kandidaten:
        return False
    # Keine Überschneidung in den Vergleichslisten
    for vlist in vergleichslisten:
        if set(kandidaten) & set(vlist[name]):
            return False
    # In jeder Spalte nur einmal pro Name
    for idx, kandidat in enumerate(kandidaten):
        if kandidat in spalte_besetzungen[idx]:
            return False
    return True

def rekursiv_zuordnen(namen, vergleichslisten, aktuelle_liste, spalte_besetzungen, i=0):
    if i >= len(namen):
        lösungen.append(deepcopy(aktuelle_liste))
        return
    name = namen[i]
    verboten = {name}
    for vlist in vergleichslisten:
        verboten.update(vlist[name])
    verfuegbar = [n for n in namen if n not in verboten]
    # Alle Kombinationen (Permutationen) der verfügbaren Namen für die Zeile durchgehen
    for kandidaten in permutations(verfuegbar, spalten_an):
        if ist_gueltig(aktuelle_liste, name, kandidaten, vergleichslisten, spalte_besetzungen):
            neue_besetzungen = deepcopy(spalte_besetzungen)
            for idx, kandidat in enumerate(kandidaten):
                neue_besetzungen[idx].add(kandidat)
            aktuelle_liste[name] = list(kandidaten)
            rekursiv_zuordnen(namen, vergleichslisten, aktuelle_liste, neue_besetzungen, i+1)
            del aktuelle_liste[name]

def loesungen_auswerten(lösungen, liste1, namen):
    statistik = []
    for loesung in lösungen:
        # Zähle Überschneidungen mit Vergleichsliste 1
        ueberschneidungen = sum(len(set(loesung[name]) & set(liste1[name])) for name in namen)
        statistik.append((loesung, ueberschneidungen))
    if not statistik:
        return None
    min_ue = min(ue for _, ue in statistik)
    beste_listen = [loesung for loesung, ue in statistik if ue == min_ue]
    return {
        'gesamt_loesungen': len(lösungen),
        'min_ueberschneidungen': min_ue,
        'anzahl_beste_listen': len(beste_listen),
        'beste_listen': beste_listen,
        'statistik': statistik
    }

# Starte das Backtracking
spalte_besetzungen = [set() for _ in range(spalten_an)]
aktuelle_liste = {}

print("Suche nach allen gültigen Listen ... (dauert!)")
rekursiv_zuordnen(namen, vergleichslisten, aktuelle_liste, spalte_besetzungen)

results = loesungen_auswerten(lösungen, liste1, namen)

if results is None:
    print("Keine passende Liste gefunden.")
else:
    print(f"\nGefundene Gesamtlisten: {results['gesamt_loesungen']}")
    print(f"Minimale Überschneidungen mit Vergleichsliste 1: {results['min_ueberschneidungen']}")
    print(f"Anzahl Listen mit minimaler Überschneidung: {results['anzahl_beste_listen']}\n")
    print("Eine beste Liste:")
    for name in namen:
        print(f"{name}: {', '.join(results['beste_listen'][0][name])}")
