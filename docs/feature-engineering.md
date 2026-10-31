# Feature engineering

## Ordre des opérations
1. Regroupement des 15 labels en 8 familles (`LabelGrouper`) et cible binaire.
2. **Découpage stratifié 80/20** par famille, avant tout apprentissage.
3. Sélection de features et normalisation, **ajustées sur le train uniquement**.
4. Application au test, écriture en Parquet.

Ajuster sur toutes les données ferait fuiter de l'information du test vers
l'entraînement et rendrait les scores optimistes.

## Familles
| Famille | Labels d'origine |
|---|---|
| BENIGN | BENIGN |
| DoS | DoS Hulk, GoldenEye, slowloris, Slowhttptest |
| DDoS | DDoS |
| PortScan | PortScan |
| BruteForce | FTP-Patator, SSH-Patator |
| WebAttack | Brute Force, XSS, SQL injection (quasi indiscernables par flux) |
| Bot | Bot |
| Rare | Infiltration, Heartbleed (moins de 50 flux) |

« Rare » est exclue de l'évaluation multi-classes, mais reste « attaque » en binaire.

## Sélection de features
Le détail (colonne par colonne) est dans `reports/tables/feature_selection.csv`.

**Résultat : 46 features retenues sur 78.**

| Étape | Retirées | Restantes |
|---|---|---|
| Départ | | 78 |
| Exclusion configurée (`destination_port`) | 1 | 77 |
| Colonnes constantes | 8 | 69 |
| Corrélation supérieure à 0,95 | 23 | 46 |

Les 8 colonnes constantes sont les six features « bulk » ainsi que `bwd_psh_flags` et
`bwd_urg_flags`. Le filtre de corrélation a confirmé les trois paires vues en EDA
(paquets avant/arrière, taille moyenne des paquets, débits de paquets) et en a
trouvé 20 autres. La sélection est calculée sur le jeu d'entraînement uniquement.

| Règle | Pourquoi |
|---|---|
| Exclusion de `destination_port` | Identifiant et non une quantité ; lie le modèle aux serveurs du banc d'essai |
| Colonnes constantes | Variance nulle : aucune information |
| Corrélation supérieure à 0,95 | Redondance (paires vues en EDA, copie exacte `fwd_header_length_1`) |

## Limites
- Pour chaque paire corrélée, `CorrelationFilter` garde la première colonne dans
  l'ordre du fichier, pas la plus informative. Les informations restent portées
  par la colonne conservée, mais le choix n'est pas guidé par le pouvoir prédictif.
- Pas d'horodatage dans ce dataset : découpage aléatoire par flux. Des flux d'une même
  session d'attaque peuvent se trouver dans le train et le test, ce qui peut
  surestimer les performances.
- Le scaler suppose des distributions proches de la normale ; or beaucoup de
  features réseau sont très asymétriques. Une transformation logarithmique est une
  amélioration possible.