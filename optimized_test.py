import time

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

# Fonction pour appliquer l'algorithme du sac à dos
def optimiser_investissements(actions, budget_max):
    # Convertir le budget en centimes pour éviter les problèmes avec les décimales
    budget_max_cents = int(budget_max * 100)
    n = len(actions)

    # Matrice pour stocker les profits maximaux
    matrix = [[0 for _ in range(budget_max_cents + 1)] for _ in range(n + 1)]

    # Remplissage de la matrice
    for i in range(1, n + 1):
        action = actions[i - 1]
        cost_cents = int(action[1] * 100)  # Coût en centimes
        profit = action[1] * action[2] / 100  # Profit calculé

        for w in range(budget_max_cents + 1):
            if cost_cents <= w:
                matrix[i][w] = max(matrix[i - 1][w], matrix[i - 1][w - cost_cents] + profit) # Prendre le maximum
            else:
                matrix[i][w] = matrix[i - 1][w] # Sinon, garder la valeur précédente

    # Extraction des actions sélectionnées et calcul du coût total investi (backtracking)
    w = budget_max_cents
    selected_actions = []
    total_cost_cents = 0  # Stocker le coût total en centimes

    for i in range(n, 0, -1):
        action = actions[i - 1]
        cost_cents = int(action[1] * 100)

        if matrix[i][w] != matrix[i - 1][w]:
            selected_actions.append(action)
            w -= cost_cents
            total_cost_cents += cost_cents  # Ajouter le coût de l'action au total

    total_cost_euros = total_cost_cents / 100  # Convertir le coût total en euros

    return selected_actions, matrix[n][budget_max_cents], total_cost_euros

# Fonction pour mesurer le temps d'exécution
def mesurer_temps_execution(fonction, *args):
    start_time = time.time()
    result = fonction(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

# Définir le budget maximum en euros
budget_max = 500

# Mesurer le temps d'exécution et appliquer l'algorithme d'optimisation
(meilleures_actions, meilleur_profit, total_investi), temps_execution = mesurer_temps_execution(optimiser_investissements, actions, budget_max)

# Afficher les résultats
print(f"Actions sélectionnées : {[action[0] for action in meilleures_actions]}")
print(f"Profit total : {meilleur_profit:.2f} euros")
print(f"Coût total investi : {total_investi:.2f} euros")
print(f"Budget maximum : {budget_max:.2f} euros")
print(f"Montant restant : {(budget_max - total_investi):.2f} euros")
print(f"Temps d'exécution : {temps_execution:.4f} secondes")
