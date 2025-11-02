import random
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import time

def count_overlaps(assignments1: Dict[str, List[str]], assignments2: Dict[str, List[str]]) -> int:
    """
    Zählt die Anzahl der Übereinstimmungen zwischen zwei Zuordnungen.
    """
    overlaps = 0
    for giver in assignments1:
        receivers1_set = set(assignments1[giver])
        receivers2_set = set(assignments2.get(giver, []))
        overlaps += len(receivers1_set & receivers2_set)
    return overlaps


class OptimizedSecretSantaSolver:
    """
    Optimierter Solver mit Iterative Deepening und erweiterten Pruning-Strategien.
    """
    
    def __init__(self, participants: List[str], rounds: int, 
                 liste1: Optional[Dict[str, List[str]]] = None,
                 liste2: Optional[Dict[str, List[str]]] = None):
        self.participants = participants
        self.n = len(participants)
        self.rounds = rounds
        self.liste1 = liste1 or {}
        self.liste2 = liste2 or {}
        
        # Vorberechnete Overlap-Informationen für schnelleres Pruning
        self.liste1_overlaps = self._precompute_overlap_matrix(liste1) if liste1 else {}
        
        # Statistiken
        self.solutions_found = []
        self.total_nodes_explored = 0
        self.total_branches_pruned = 0
        self.search_start_time = None
        
    def _precompute_overlap_matrix(self, liste: Dict[str, List[str]]) -> Dict[Tuple[str, str], bool]:
        """
        Vorberechnung: Welche Giver->Receiver Paare existieren in der Liste?
        O(1) Lookup statt O(n) bei jedem Check.
        """
        overlap_set = {}
        for giver, receivers in liste.items():
            for receiver in receivers:
                overlap_set[(giver, receiver)] = True
        return overlap_set
    
    def solve(self, max_solutions_per_level: int = 1000000) -> Optional[Dict]:
        """
        Iterative Deepening: Suche zuerst nach Lösungen mit 0 Überschneidungen,
        dann 1, dann 2, etc. Stoppt beim ersten erfolgreichen Level.
        
        Args:
            max_solutions_per_level: Maximale Anzahl Lösungen pro Overlap-Level
        """
        self.search_start_time = time.time()
        self.max_solutions = max_solutions_per_level
        
        print(f"{'='*70}")
        print(f"OPTIMIERTE SYSTEMATISCHE SUCHE - ITERATIVE DEEPENING")
        print(f"{'='*70}")
        print(f"Teilnehmer: {self.n}, Runden: {self.rounds}")
        print(f"Sammle maximal {max_solutions_per_level:,} Lösungen pro Level\n")
        
        # Theoretisches Maximum: jeder könnte alle 3 überschneiden
        max_possible_overlap = self.n * self.rounds
        
        # Iterative Deepening: Versuche jedes Overlap-Level
        for target_overlap in range(max_possible_overlap + 1):
            print(f"{'─'*70}")
            print(f"Suche nach Lösungen mit maximal {target_overlap} Überschneidungen zu Liste 1...")
            print(f"{'─'*70}")
            
            self.solutions_found = []
            self.total_nodes_explored = 0
            self.total_branches_pruned = 0
            level_start_time = time.time()
            
            # Suche mit diesem Overlap-Limit
            self._backtrack_all_rounds(target_overlap)
            
            level_elapsed = time.time() - level_start_time
            
            # Neue Zeile nach dem Progress-Update
            if self.solutions_found:
                print()  # Neue Zeile nach der letzten \r-Ausgabe
            
            print(f"\n  Ergebnis für Overlap-Level {target_overlap}:")
            print(f"  • Knoten erkundet: {self.total_nodes_explored:,}")
            print(f"  • Branches gepruned: {self.total_branches_pruned:,}")
            print(f"  • Zeit: {level_elapsed:.2f}s")
            print(f"  • Lösungen gefunden: {len(self.solutions_found)}")
            
            # Wenn wir Lösungen gefunden haben, sind wir fertig!
            if self.solutions_found:
                print(f"\n✓ Optimales Overlap-Level gefunden: {target_overlap}")
                break
        
        total_elapsed = time.time() - self.search_start_time
        
        if not self.solutions_found:
            print(f"\n❌ Keine gültige Lösung gefunden!")
            return None
        
        x = target_overlap
        candidates_with_x = self.solutions_found
        
        print(f"\n{'='*70}")
        print(f"SUCHE ABGESCHLOSSEN")
        print(f"{'='*70}\n")
        
        print(f"📊 ERGEBNISSE - Überschneidungen mit Liste 1:")
        print(f"   Minimale Überschneidungen (x): {x}")
        print(f"   Anzahl Listen mit {x} Überschneidungen: {len(candidates_with_x)}")
        
        # Wenn liste2 gegeben, finde beste bzgl. liste2
        if self.liste2:
            min_overlap_liste2 = float('inf')
            best_candidates = []
            overlap2_counts = defaultdict(int)
            
            print(f"\n   Analysiere Überschneidungen mit Liste 2...")
            for candidate in candidates_with_x:
                overlap2 = count_overlaps(candidate, self.liste2)
                overlap2_counts[overlap2] += 1
                
                if overlap2 < min_overlap_liste2:
                    min_overlap_liste2 = overlap2
                    best_candidates = [candidate]
                elif overlap2 == min_overlap_liste2:
                    best_candidates.append(candidate)
            
            print(f"\n📊 ERGEBNISSE - Überschneidungen mit Liste 2:")
            print(f"   Minimale Überschneidungen: {min_overlap_liste2}")
            print(f"   Anzahl Listen mit {min_overlap_liste2} Überschneidungen: {len(best_candidates)}")
            
            print(f"\n📊 Verteilung der Überschneidungen mit Liste 2:")
            for overlap_count in sorted(overlap2_counts.keys()):
                count = overlap2_counts[overlap_count]
                percentage = (count / len(candidates_with_x)) * 100
                bar = "█" * min(40, int(percentage))
                print(f"   {overlap_count:2d} Überschneidungen: {count:5d} Listen ({percentage:5.1f}%) {bar}")
            
            chosen_assignment = random.choice(best_candidates)
            
            return {
                'assignment': chosen_assignment,
                'overlap_liste1': x,
                'total_with_x_overlap_liste1': len(candidates_with_x),
                'overlap_liste2': min_overlap_liste2,
                'total_with_min_overlap_liste2': len(best_candidates),
                'nodes_explored': self.total_nodes_explored,
                'branches_pruned': self.total_branches_pruned,
                'time_elapsed': total_elapsed,
                'all_candidates_with_x': candidates_with_x
            }
        else:
            chosen_assignment = random.choice(candidates_with_x)
            
            return {
                'assignment': chosen_assignment,
                'overlap_liste1': x,
                'total_with_x_overlap_liste1': len(candidates_with_x),
                'nodes_explored': self.total_nodes_explored,
                'branches_pruned': self.total_branches_pruned,
                'time_elapsed': total_elapsed,
                'all_candidates_with_x': candidates_with_x
            }
    
    def _backtrack_all_rounds(self, max_overlap: int):
        """
        Backtracking über alle Runden mit Overlap-Limit.
        """
        assignment = {p: [] for p in self.participants}
        current_overlap = 0
        self._backtrack_rounds(assignment, 0, current_overlap, max_overlap)
    
    def _backtrack_rounds(self, assignment: Dict[str, List[str]], round_idx: int,
                          current_overlap: int, max_overlap: int):
        """
        Rekursives Backtracking für Runden mit Overlap-Tracking.
        """
        # Abbruch, wenn wir genug Lösungen haben
        if len(self.solutions_found) >= self.max_solutions:
            return
        
        # DEBUG für erste paar Runden-Übergänge
        if len(self.solutions_found) < 3 and round_idx > 0:
            print(f"\n  DEBUG - Starte Runde {round_idx}:")
            print(f"    Current_overlap: {current_overlap}")
            for giver in sorted(assignment.keys())[:3]:
                print(f"    {giver}: {assignment[giver]} (Länge: {len(assignment[giver])})")
        
        if round_idx == self.rounds:
            # Lösung gefunden! Validiere sie erst
            actual_overlap = count_overlaps(assignment, self.liste1)
            
            # DEBUG: Zeige erste paar Lösungen
            if len(self.solutions_found) < 3:
                print(f"\n  DEBUG - Lösung #{len(self.solutions_found) + 1} KOMPLETT:")
                print(f"  Current_overlap tracking: {current_overlap}")
                print(f"  Tatsächlicher Overlap: {actual_overlap}")
                for giver in sorted(assignment.keys()):
                    print(f"    {giver}: {assignment[giver]}")
            
            if actual_overlap != current_overlap:
                print(f"\n  ⚠️  FEHLER: Overlap-Tracking stimmt nicht!")
                print(f"  Getrackt: {current_overlap}, Tatsächlich: {actual_overlap}")
                return
            
            solution_copy = {k: v.copy() for k, v in assignment.items()}
            self.solutions_found.append(solution_copy)
            
            if len(self.solutions_found) % 100 == 0:
                elapsed = time.time() - self.search_start_time
                print(f"\r  Lösungen gefunden: {len(self.solutions_found):,} ({elapsed:.1f}s)", end='', flush=True)
            
            # Abbruch nach dieser Lösung prüfen
            if len(self.solutions_found) >= self.max_solutions:
                print(f"\n  ✓ Limit von {self.max_solutions:,} Lösungen erreicht, stoppe Suche")
            
            return
        
        # Generiere Permutationen für diese Runde
        self._generate_round_permutations(assignment, round_idx, current_overlap, max_overlap)
    
    def _generate_round_permutations(self, assignment: Dict[str, List[str]], 
                                     round_idx: int, current_overlap: int, max_overlap: int):
        """
        Generiert Permutationen mit optimiertem Pruning.
        """
        receivers_used = set()
        givers = self.participants.copy()
        
        self._permute_receivers(assignment, round_idx, givers, 0, receivers_used, 
                               current_overlap, max_overlap)
    
    def _permute_receivers(self, assignment: Dict[str, List[str]], round_idx: int,
                          givers: List[str], giver_idx: int, receivers_used: Set[str],
                          current_overlap: int, max_overlap: int):
        """
        Rekursives Permutieren mit erweiterten Pruning-Strategien.
        """
        # Abbruch, wenn wir genug Lösungen haben
        if len(self.solutions_found) >= self.max_solutions:
            return
        
        self.total_nodes_explored += 1
        
        # DEBUG: Zeige ersten paar Knoten NUR in Runde 0
        if self.total_nodes_explored <= 20 and round_idx == 0:
            print(f"\n  DEBUG Node {self.total_nodes_explored}:")
            print(f"    Round: {round_idx}, Giver_idx: {giver_idx}/{len(givers)}")
            print(f"    Current_overlap: {current_overlap}, Max: {max_overlap}")
            print(f"    Receivers_used: {receivers_used}")
        
        if giver_idx == len(givers):
            # Runde komplett - weiter zur nächsten
            if self.total_nodes_explored <= 20 and round_idx == 0:
                print(f"    -> Runde {round_idx} komplett, gehe zu Runde {round_idx + 1}")
            self._backtrack_rounds(assignment, round_idx + 1, current_overlap, max_overlap)
            return
        
        giver = givers[giver_idx]
        already_received = set(assignment[giver])  # Optimierung: Set für O(1) lookup
        
        # Vorberechnung für Constraint Propagation
        available_receivers = []
        for receiver in self.participants:
            # Basis-Constraints
            if receiver == giver or receiver in already_received or receiver in receivers_used:
                continue
            available_receivers.append(receiver)
        
        if self.total_nodes_explored <= 20 and round_idx == 0:
            print(f"    Giver: {giver}, Available receivers: {available_receivers}")
        
        # Constraint Propagation: Prüfe ob verbleibende Giver noch genug Optionen haben
        if not self._check_feasibility(assignment, round_idx, giver_idx, givers, receivers_used):
            self.total_branches_pruned += 1
            if self.total_nodes_explored <= 20 and round_idx == 0:
                print(f"    -> PRUNED (feasibility)")
            return
        
        # Versuche jeden verfügbaren Empfänger
        for receiver in available_receivers:
            # Pruning: Würde diese Zuordnung das Overlap-Limit überschreiten?
            would_add_overlap = (giver, receiver) in self.liste1_overlaps
            new_overlap = current_overlap + (1 if would_add_overlap else 0)
            
            if self.total_nodes_explored <= 20 and round_idx == 0:
                print(f"    Trying {giver} -> {receiver}: would_overlap={would_add_overlap}, new_overlap={new_overlap}")
            
            if new_overlap > max_overlap:
                self.total_branches_pruned += 1
                if self.total_nodes_explored <= 20 and round_idx == 0:
                    print(f"      -> PRUNED (overlap limit)")
                continue
            
            # Zuordnung hinzufügen
            assignment[giver].append(receiver)
            receivers_used.add(receiver)
            
            if self.total_nodes_explored <= 20 and round_idx == 0:
                print(f"      -> Assigned, recurse...")
            
            # Rekursiv weiter
            self._permute_receivers(assignment, round_idx, givers, giver_idx + 1, 
                                   receivers_used, new_overlap, max_overlap)
            
            # Backtrack
            assignment[giver].pop()
            receivers_used.remove(receiver)
    
    def _check_feasibility(self, assignment: Dict[str, List[str]], round_idx: int,
                          current_giver_idx: int, givers: List[str], 
                          receivers_used: Set[str]) -> bool:
        """
        Constraint Propagation: Prüfe ob noch genug Empfänger für verbleibende Giver da sind.
        Verhindert sinnlose Branches, die später scheitern würden.
        """
        remaining_givers = givers[current_giver_idx + 1:]
        available_receivers = set(self.participants) - receivers_used
        
        # Für jeden verbleibenden Giver prüfen, ob mindestens 1 Option existiert
        for future_giver in remaining_givers:
            already_received = set(assignment[future_giver])
            valid_options = available_receivers - {future_giver} - already_received
            
            if not valid_options:
                # Dieser Giver hätte keine gültige Option mehr
                return False
        
        return True


def print_assignments(assignments: Dict[str, List[str]], title: str = "SECRET SANTA ZUORDNUNGEN"):
    """Gibt die Zuordnungen übersichtlich aus"""
    print("\n" + "="*70)
    print(title)
    print("="*70)
    
    print(f"\n{'Schenker':<15} | Runde 1       | Runde 2       | Runde 3")
    print("-" * 70)
    
    for giver, receivers in sorted(assignments.items()):
        receivers_str = " | ".join(f"{r:<13}" for r in receivers)
        print(f"{giver:<15} | {receivers_str}")
    
    print("="*70)


def print_comparison(new_list: Dict[str, List[str]], old_list: Dict[str, List[str]], year: str):
    """Zeigt die Überschneidungen zwischen zwei Listen"""
    print(f"\n🔍 Vergleich mit {year}:")
    overlaps = []
    for giver in sorted(new_list.keys()):
        new_receivers = set(new_list[giver])
        old_receivers = set(old_list.get(giver, []))
        common = new_receivers & old_receivers
        if common:
            overlaps.append((giver, list(common)))
    
    if overlaps:
        for giver, receivers in overlaps:
            print(f"   {giver} beschenkt wieder: {', '.join(receivers)}")
    else:
        print(f"   ✓ Keine Überschneidungen!")
    
    print(f"   Gesamt: {count_overlaps(new_list, old_list)} Überschneidungen")


# Beispielverwendung
if __name__ == "__main__":
    teilnehmer = [
        "Jannes", "Abdalla", "Christian", "Lea L", 
        "Esther", "Charlotte", "Sébastien", "Stephanie", "Lea D"
    ]
    
    # Beispiel Listen aus Vorjahren (hart kodiert) - nur 8 Teilnehmer
    liste1_vorjahr = {
        'Jannes': ['Charlotte', 'Stephanie', 'Lea L'],
        'Abdalla': ['Jannes', 'Sébastien', 'Esther'],
        'Christian': ['Stephanie', 'Esther', 'Sébastien'],
        'Lea L': ['Esther', 'Abdalla', 'Christian'],
        'Esther': ['Lea L', 'Charlotte', 'Jannes'],
        'Charlotte': ['Christian', 'Jannes', 'Stephanie'],
        'Sébastien': ['Charlotte', 'Lea L', 'Abdalla'],
        'Stephanie': ['Sébastien', 'Christian', 'Abdalla']
    }
    
    liste2_vorvorjahr = {
        'Jannes': ['Esther', 'Lea L', 'Sébastien'],
        'Abdalla': ['Charlotte', 'Stephanie', 'Esther'],
        'Christian': ['Lea L', 'Charlotte', 'Stephanie'],
        'Lea L': ['Abdalla', 'Sébastien', 'Jannes'],
        'Esther': ['Christian', 'Abdalla', 'Charlotte'],
        'Charlotte': ['Sébastien', 'Jannes', 'Abdalla'],
        'Sébastien': ['Stephanie', 'Christian', 'Lea L'],
        'Stephanie': ['Jannes', 'Esther', 'Christian']
    }
    
    print("="*70)
    print("SECRET SANTA OPTIMIERUNG - ITERATIVE DEEPENING")
    print("="*70)
    
    # Zeige Vorjahres-Listen
    print_assignments(liste1_vorjahr, "LISTE 1 - VORJAHR")
    print_assignments(liste2_vorvorjahr, "LISTE 2 - VORVORJAHR")
    
    # Erstelle optimierten Solver
    solver = OptimizedSecretSantaSolver(
        participants=teilnehmer,
        rounds=3,
        liste1=liste1_vorjahr,
        liste2=liste2_vorvorjahr
    )
    
    # Finde optimale Lösung
    result = solver.solve()
    
    if result:
        # Zeige gewählte Liste
        print_assignments(result['assignment'], "NEUE LISTE - OPTIMAL")
        
        # Detaillierter Vergleich
        print_comparison(result['assignment'], liste1_vorjahr, "Liste 1 (Vorjahr)")
        print_comparison(result['assignment'], liste2_vorvorjahr, "Liste 2 (Vorvorjahr)")
        
        # Zusammenfassung
        print("\n" + "="*70)
        print("📋 ZUSAMMENFASSUNG")
        print("="*70)
        print(f"✓ Minimale Überschneidungen mit Liste 1 (x): {result['overlap_liste1']}")
        print(f"✓ Listen mit {result['overlap_liste1']} Überschneidungen gefunden: {result['total_with_x_overlap_liste1']}")
        if 'overlap_liste2' in result:
            print(f"✓ Überschneidungen der gewählten Liste mit Liste 2: {result['overlap_liste2']}")
            print(f"✓ Weitere Listen mit {result['overlap_liste2']} Überschneidungen zu Liste 2: {result['total_with_min_overlap_liste2'] - 1}")
        print(f"✓ Knoten erkundet: {result['nodes_explored']:,}")
        print(f"✓ Branches gepruned: {result['branches_pruned']:,}")
        print(f"✓ Gesamtrechenzeit: {result['time_elapsed']:.2f} Sekunden")
        print("="*70)