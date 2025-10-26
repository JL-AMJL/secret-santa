import random
from collections import defaultdict

# Liste 2 (Referenz)
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

namen = ['Jannes', 'Abdalla', 'Christian', 'Lea', 'Esther', 'Charlotte', 'Sébastien', 'Stephanie']

def ist_gueltig(zuordnung, name, kandidaten, liste2):
    """Prüft, ob die Zuordnung alle Regeln erfüllt"""
    # Regel 1: Kein Name darf sich wiederholen
    if len(kandidaten) != len(set(kandidaten)):
        return False
    
    # Regel 2: Zeilenname darf nicht in den Kandidaten sein
    if name in kandidaten:
        return False
    
    # Regel 3: Keine Überschneidung mit Liste 2
    liste2_namen = set(liste2[name])
    if len(set(kandidaten) & liste2_namen) > 0:
        return False
    
    # Regel 4: Spalten-Check (jeder Name muss in jeder Spalte vorkommen)
    for i, kandidat in enumerate(kandidaten):
        spalte = i
        # Zähle, wie oft dieser Name schon in dieser Spalte vorkommt
        count = sum(1 for n in zuordnung if len(zuordnung[n]) > spalte and zuordnung[n][spalte] == kandidat)
        # Wenn ein Name schon zu oft in dieser Spalte ist
        if count > 1:  # Maximal einmal pro Spalte (außer aktuelle Zeile)
            return False
    
    return True

def erstelle_liste_backtracking(namen, liste2, max_versuche=10000):
    """Erstellt eine Liste mit Backtracking-Algorithmus"""
    
    for versuch in range(max_versuche):
        zuordnung = {}
        erfolg = True
        
        # Shuffeln für Variation
        namen_reihenfolge = namen.copy()
        random.shuffle(namen_reihenfolge)
        
        for name in namen_reihenfolge:
            # Verfügbare Namen (alle außer dem Zeilennamen und die aus Liste 2)
            verfuegbar = [n for n in namen if n != name and n not in liste2[name]]
            
            gefunden = False
            attempts = 0
            max_attempts = 1000
            
            while not gefunden and attempts < max_attempts:
                attempts += 1
                random.shuffle(verfuegbar)
                
                # Wähle 3 Namen
                if len(verfuegbar) < 3:
                    break
                    
                kandidaten = verfuegbar[:3]
                
                # Temporäre Zuordnung
                zuordnung[name] = kandidaten
                
                # Prüfe Spalten-Constraint
                spalten_ok = True
                for i in range(3):
                    spalte_namen = [zuordnung[n][i] for n in zuordnung if len(zuordnung[n]) > i]
                    if len(spalte_namen) != len(set(spalte_namen)):
                        spalten_ok = False
                        break
                
                if spalten_ok and ist_gueltig(zuordnung, name, kandidaten, liste2):
                    gefunden = True
                    break
                else:
                    del zuordnung[name]
            
            if not gefunden:
                erfolg = False
                break
        
        if erfolg and len(zuordnung) == 8:
            # Finale Validierung: Jede Spalte muss alle 8 Namen enthalten
            spalten_valid = True
            for i in range(3):
                spalte = [zuordnung[n][i] for n in namen]
                if set(spalte) != set(namen):
                    spalten_valid = False
                    break
            
            if spalten_valid:
                return zuordnung
    
    return None

# Erstelle die Liste
print("Suche nach einer passenden Liste...")
print("(Dies kann einen Moment dauern...)\n")

neue_liste = erstelle_liste_backtracking(namen, liste2, max_versuche=50000)

if neue_liste:
    print("Erfolg! Hier ist die neue Liste:\n")
    for name in namen:  # In der Reihenfolge von Liste 2
        print(f"{name}: {', '.join(neue_liste[name])}")
    
    # Überprüfe Überschneidungen
    print("\n--- Überprüfung ---")
    ueberschneidungen = 0
    for name in namen:
        gemeinsam = set(neue_liste[name]) & set(liste2[name])
        ueberschneidungen += len(gemeinsam)
        if gemeinsam:
            print(f"{name}: {gemeinsam}")
    
    print(f"\nGesamte Überschneidungen: {ueberschneidungen}")
    
    # Überprüfe Spalten
    print("\n--- Spaltenvalidierung ---")
    for i in range(3):
        spalte = [neue_liste[n][i] for n in namen]
        print(f"Spalte {i+1}: {set(spalte)} (Länge: {len(set(spalte))})")
else:
    print("Keine passende Liste gefunden. Versuche es mit mehr Durchläufen.")
