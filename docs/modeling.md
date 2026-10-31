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
Jeu de test : 504 152 flux, distribution réelle (83,1 % de trafic bénin).

| Expérience | Accuracy | F1 macro |
|---|---|---|
| Binaire, régression logistique | 0,954 | 0,921 |
| Binaire, Random Forest | 0,997 | 0,995 |
| Familles, régression logistique | 0,965 | 0,591 |
| Familles, Random Forest | 0,997 | 0,925 |
| Familles, Random Forest sans features suspectes | 0,997 | 0,926 |

- La régression logistique atteint 96,5 % d'accuracy en familles mais seulement
  0,59 de F1 macro : l'accuracy masque l'échec sur les classes minoritaires.
- Le Random Forest améliore le F1 macro de 0,33 en familles.
- F1 par classe (Random Forest) : BENIGN 0,998, DDoS 0,999, PortScan 0,994,
  DoS 0,989, BruteForce 0,983, WebAttack 0,934, Bot 0,580.
- Bot est le point faible : précision et rappel proches de 0,58 pour 390 flux de test.
  Sans cette classe, le F1 macro des six autres serait de 0,983.
- WebAttack : précision de 0,987 mais rappel de 0,886 (environ 11 % manqués).

## Test d'ablation
Entraînement sans `init_win_bytes_forward`, `init_win_bytes_backward` et
`psh_flag_count`, suspectes d'encoder l'outil de l'émetteur plus que son comportement.
Résultat : le F1 macro passe de 0,9252 à 0,9257 (accuracy 0,9969 à 0,9965), soit une
différence négligeable. Le modèle n'a donc pas besoin de ces trois features.

Ce que cela ne démontre pas : l'absence de tout raccourci. D'autres features peuvent
porter la même information, et un seul découpage avec une seule graine ne permet
pas de conclure à une équivalence stricte.
## Limites
- Un seul découpage aléatoire, pas de validation croisée.
- Le fichier utilisé n'a ni adresses IP ni horodatage : pas de features agrégées dans
  le temps (par exemple la périodicité d'un botnet), ce qui explique probablement en
  partie la faiblesse sur la classe Bot (hypothèse).
- Le bon score sur WebAttack vient en partie du regroupement de trois attaques en une
  famille : il ne prouve pas que le modèle distingue XSS, injection SQL et brute force web.
- Pas d'horodatage : des flux d'une même session d'attaque peuvent se trouver
  dans le train et le test (scores probablement optimistes).
- Hyperparamètres choisis a priori, sans recherche.
- Dataset capturé en banc d'essai contrôlé : la généralisation au trafic réel n'est pas démontrée.