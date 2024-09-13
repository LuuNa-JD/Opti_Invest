import time
import itertools

# Jeu de données
actions = [
    ("Action-1", 20, 5),
    ("Action-2", 30, 10),
    ("Action-3", 50, 15),
    ("Action-4", 70, 20),
    ("Action-5", 60, 17),
    ("Action-6", 80, 25),
    ("Action-7", 22, 7),
    ("Action-8", 26, 11),
    ("Action-9", 48, 13),
    ("Action-10", 34, 27),
    ("Action-11", 42, 17),
    ("Action-12", 110, 9),
    ("Action-13", 38, 23),
    ("Action-14", 14, 1),
    ("Action-15", 18, 3),
    ("Action-16", 8, 8),
    ("Action-17", 4, 12),
    ("Action-18", 10, 14),
    ("Action-19", 24, 21),
    ("Action-20", 114, 18)
]

# Algorithme brute-force
def bruteforce(actions, budget_max):
    best_profit = 0
    best_combination = []

    # Générer toutes les combinaisons possibles d'actions
    for r in range(1, len(actions) + 1):
        for combination in itertools.combinations(actions, r):
            total_cost = sum(action[1] for action in combination)
            if total_cost <= budget_max:  # Vérifier que la combinaison respecte le budget
                total_profit = sum(action[1] * action[2] / 100 for action in combination)
                # Mettre à jour la meilleure combinaison si le profit est supérieur
                if total_profit > best_profit:
                    best_profit = total_profit
                    best_combination = combination

    total_cost = sum(action[1] for action in best_combination)
    return best_combination, best_profit, total_cost

# Fonction pour mesurer le temps d'exécution
def mesurer_temps_execution(fonction, *args):
    start_time = time.time()  # Enregistre l'heure de début
    result = fonction(*args)  # Exécute la fonction avec ses arguments
    end_time = time.time()  # Enregistre l'heure de fin
    elapsed_time = end_time - start_time  # Calcule le temps écoulé
    return result, elapsed_time

# Définir le budget maximum en euros
budget_max = 500

# Mesurer le temps d'exécution et appliquer l'algorithme brute-force
(meilleures_actions, meilleur_profit, total_investi), temps_execution = mesurer_temps_execution(bruteforce, actions, budget_max)

# Afficher les résultats
print(f"Actions sélectionnées : {[action[0] for action in meilleures_actions]}")
print(f"Profit total : {meilleur_profit:.2f} euros")
print(f"Coût total investi : {total_investi:.2f} euros")
print(f"Budget maximum : {budget_max:.2f} euros")
print(f"Montant restant : {(budget_max - total_investi):.2f} euros")
print(f"Temps d'exécution : {temps_execution:.4f} secondes")
