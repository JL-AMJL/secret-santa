import random
from typing import List, Dict, Set

def generate_secret_santa(participants: List[str], rounds: int = 3, max_attempts: int = 1000) -> Dict[str, List[str]]:
    """
    Generiert eine Secret Santa Zuordnung mit mehreren Runden.
    
    Args:
        participants: Liste der Teilnehmernamen
        rounds: Anzahl der Runden (jeder beschenkt X Personen)
        max_attempts: Maximale Versuche für die Generierung
    
    Returns:
        Dictionary mit Teilnehmer als Key und Liste der zu beschenkenden Personen
    """
    n = len(participants)
    
    if n < rounds + 1:
        raise ValueError(f"Mindestens {rounds + 1} Teilnehmer erforderlich für {rounds} Runden")
    
    for attempt in range(max_attempts):
        try:
            assignments = {p: [] for p in participants}
            
            # Für jede Runde
            for round_num in range(rounds):
                # Erstelle eine Permutation für diese Runde
                givers = participants.copy()
                receivers = participants.copy()
                random.shuffle(receivers)
                
                # Prüfe und korrigiere die Permutation
                for i, giver in enumerate(givers):
                    receiver = receivers[i]
                    attempts_fix = 0
                    
                    # Stelle sicher, dass niemand sich selbst beschenkt
                    # und niemand jemanden zweimal beschenkt
                    while (receiver == giver or receiver in assignments[giver]) and attempts_fix < n * 2:
                        # Tausche mit einer zufälligen anderen Position
                        swap_idx = random.randint(0, n - 1)
                        receivers[i], receivers[swap_idx] = receivers[swap_idx], receivers[i]
                        receiver = receivers[i]
                        attempts_fix += 1
                    
                    if receiver == giver or receiver in assignments[giver]:
                        # Dieser Versuch ist fehlgeschlagen
                        raise ValueError("Keine gültige Zuordnung gefunden")
                    
                    assignments[giver].append(receiver)
                
                # Validiere diese Runde: Jeder muss genau einmal als Empfänger vorkommen
                receivers_count = {}
                for receiver_list in assignments.values():
                    if len(receiver_list) == round_num + 1:
                        last_receiver = receiver_list[-1]
                        receivers_count[last_receiver] = receivers_count.get(last_receiver, 0) + 1
                
                if any(count != 1 for count in receivers_count.values()) or len(receivers_count) != n:
                    raise ValueError("Ungültige Verteilung der Empfänger")
            
            return assignments
            
        except ValueError:
            # Dieser Versuch ist fehlgeschlagen, versuche es erneut
            continue
    
    raise RuntimeError(f"Konnte keine gültige Zuordnung nach {max_attempts} Versuchen finden")


def print_assignments(assignments: Dict[str, List[str]]):
    """Gibt die Zuordnungen übersichtlich aus"""
    print("\n" + "="*60)
    print("SECRET SANTA ZUORDNUNGEN")
    print("="*60)
    
    # Header für die Tabelle
    print(f"\n{'Schenker':<15} | Runde 1       | Runde 2       | Runde 3")
    print("-" * 60)
    
    for giver, receivers in sorted(assignments.items()):
        receivers_str = " | ".join(f"{r:<13}" for r in receivers)
        print(f"{giver:<15} | {receivers_str}")
    
    print("\n" + "="*60)


def validate_assignments(assignments: Dict[str, List[str]], participants: List[str], rounds: int) -> bool:
    """Validiert die Zuordnungen"""
    print("\nValidierung:")
    
    # 1. Jeder hat genau 'rounds' Zuordnungen
    for giver, receivers in assignments.items():
        if len(receivers) != rounds:
            print(f"❌ {giver} hat {len(receivers)} statt {rounds} Zuordnungen")
            return False
    print(f"✓ Jeder Teilnehmer beschenkt {rounds} Personen")
    
    # 2. Niemand beschenkt sich selbst
    for giver, receivers in assignments.items():
        if giver in receivers:
            print(f"❌ {giver} beschenkt sich selbst")
            return False
    print("✓ Niemand beschenkt sich selbst")
    
    # 3. Niemand beschenkt jemanden zweimal
    for giver, receivers in assignments.items():
        if len(receivers) != len(set(receivers)):
            print(f"❌ {giver} beschenkt jemanden mehrfach")
            return False
    print("✓ Niemand beschenkt jemanden mehrfach")
    
    # 4. In jeder Runde erhält jeder Teilnehmer genau ein Geschenk
    for round_num in range(rounds):
        receivers_in_round = [receivers[round_num] for receivers in assignments.values()]
        if len(receivers_in_round) != len(set(receivers_in_round)):
            print(f"❌ Runde {round_num + 1}: Manche erhalten mehrere Geschenke")
            return False
        if set(receivers_in_round) != set(participants):
            print(f"❌ Runde {round_num + 1}: Nicht alle erhalten ein Geschenk")
            return False
    print(f"✓ In jeder Runde erhält jeder genau ein Geschenk")
    
    print("\n✅ Alle Validierungen erfolgreich!")
    return True


# Beispielverwendung
if __name__ == "__main__":
    # 9 Teilnehmer
    teilnehmer = [
        "Alice", "Bob", "Charlie", "Diana", 
        "Eva", "Frank", "Grace", "Henry"
    ]
    
    print(f"Generiere Secret Santa für {len(teilnehmer)} Teilnehmer mit 3 Runden...\n")
    
    # Generiere die Zuordnungen
    zuordnungen = generate_secret_santa(teilnehmer, rounds=3)
    
    # Zeige die Zuordnungen
    print_assignments(zuordnungen)
    
    # Validiere die Zuordnungen
    validate_assignments(zuordnungen, teilnehmer, rounds=3)