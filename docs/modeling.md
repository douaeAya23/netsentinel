# Modélisation

## Tâches
- **Binaire** : BENIGN contre ATTACK (toutes familles, Rare incluse).
- **Familles** : 7 classes ; Rare (Infiltration, Heartbleed) est exclue car
  inévaluable (moins de 50 flux).

## Modèles
| Modèle | Rôle |
|---|---|
| Régression logistique | Baseline linéaire |
| Random Forest (30 arbres, profondeur 12) | Modèle non linéaire à base d'arbres |

## Entraînement sur un échantillon plafonné
Entraîner sur 2 M de lignes dépasse les ressources d'un poste local. Le jeu
d'entraînement est donc plafonné (400 000 flux bénins, 60 000 par famille
d'attaque), **mais le jeu de test garde sa distribution réelle** : les métriques
reflètent le trafic tel qu'il est. Effet attendu : un rappel élevé et une
précision légèrement plus faible sur les attaques, car le modèle voit plus
d'attaques à l'entraînement qu'en réalité.

## Métriques
Accuracy (trompeuse : 83 % de trafic bénin), **F1 macro** (moyenne des F1 par
classe), précision et rappel par classe, matrice de confusion normalisée.

## Résultats
_À compléter depuis `reports/tables/model_comparison.csv`._

## Test d'ablation
Entraînement sans `init_win_bytes_forward`, `init_win_bytes_backward` et
`psh_flag_count`, suspectes d'encoder l'outil de l'émetteur plus que son comportement.
_À compléter : variation du F1 macro et interprétation._

## Limites
- Un seul découpage aléatoire, pas de validation croisée.
- Pas d'horodatage : des flux d'une même session d'attaque peuvent se trouver
  dans le train et le test (scores probablement optimistes).
- Hyperparamètres choisis a priori, sans recherche.
- Dataset capturé en banc d'essai contrôlé : la généralisation au trafic réel n'est pas démontrée.