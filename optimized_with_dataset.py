import csv
import pandas as pd
import time

# Fonction pour lire un dataset CSV et adapter les noms des colonnes
def lire_dataset(fichier):
    data = pd.read_csv(fichier)
    data.columns = ['name', 'price', 'profit']
    return data

# Fonction pour nettoyer les données et éliminer les coûts ou profits négatifs
def nettoyer_donnees(actions):
    actions_nettoyees = actions[(actions['price'] > 0) & (actions['profit'] > 0)]
    return actions_nettoyees

# Fonction pour appliquer l'algorithme du sac à dos
def optimiser_investissements(actions, budget_max):
    actions = list(actions.itertuples(index=False, name=None))

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

    # Extraction des actions sélectionnées et calcul du coût total investi
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

# Fonction pour sauvegarder les résultats dans un CSV
def sauvegarder_resultats(nom_fichier, meilleures_actions, profit_total, total_investi, budget_max):
    with open(nom_fichier, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nom', 'Coût', 'Bénéfice'])
        for action in meilleures_actions:
            writer.writerow([action[0], action[1], action[2]])
        writer.writerow(['Profit total après 2 ans', f'{profit_total:.2f} euros'])
        writer.writerow(['Coût total investi', f'{total_investi:.2f} euros'])
        writer.writerow(['Budget maximum', f'{budget_max:.2f} euros'])
        writer.writerow(['Montant restant', f'{(budget_max - total_investi):.2f} euros'])

# Fonction pour mesurer le temps d'exécution
def mesurer_temps_execution(fonction, *args):
    start_time = time.time()
    result = fonction(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

# Charger deux datasets
dataset1 = lire_dataset('dataset1.csv')
dataset2 = lire_dataset('dataset2.csv')

# Nettoyer les deux datasets pour exclure les coûts et profits négatifs
dataset1_nettoye = nettoyer_donnees(dataset1)
dataset2_nettoye = nettoyer_donnees(dataset2)

# Définir le budget maximum en euros
budget_max = float(input("Veuillez entrer le budget maximum en euros : "))

# Mesurer le temps d'exécution et appliquer l'algorithme d'optimisation sur les deux datasets nettoyés
(meilleures_actions1, meilleur_profit1, total_investi1), temps_execution1 = mesurer_temps_execution(optimiser_investissements, dataset1_nettoye, budget_max)
(meilleures_actions2, meilleur_profit2, total_investi2), temps_execution2 = mesurer_temps_execution(optimiser_investissements, dataset2_nettoye, budget_max)

# Sauvegarder les résultats dans des fichiers CSV
sauvegarder_resultats('resultats_dataset1_opti.csv', meilleures_actions1, meilleur_profit1, total_investi1, budget_max)
sauvegarder_resultats('resultats_dataset2_opti.csv', meilleures_actions2, meilleur_profit2, total_investi2, budget_max)

# Afficher les temps d'exécution
print(f"Temps d'exécution pour dataset1 : {temps_execution1:.4f} secondes")
print(f"Temps d'exécution pour dataset2 : {temps_execution2:.4f} secondes")

print("Résultats sauvegardés avec succès dans deux fichiers CSV.")
