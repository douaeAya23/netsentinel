# Constats de l'analyse exploratoire

## Volume et nettoyage
- 2 520 798 flux après nettoyage, contre 2 830 743 dans le dataset d'origine
  (environ 11 % retirés : doublons, valeurs infinies ou manquantes).
- La perte est plus forte pour les attaques (environ 24 %) que pour le trafic
  bénin (environ 8 %). Hypothèse : les outils d'attaque automatisés produisent
  des flux identiques, supprimés comme doublons. À vérifier par classe.

## Déséquilibre des classes
- BENIGN représente 83,1 % des flux : prédire toujours « normal » donnerait
  83 % d'accuracy sans rien détecter.
- DoS Hulk, DDoS et PortScan couvrent 15,5 % des flux ; les 11 autres classes
  d'attaque, moins de 1,5 % au total.
- Heartbleed (11 flux), Web Attack - Sql Injection (21) et Infiltration (36)
  sont trop rares pour être évaluées de façon fiable.

## Conséquences pour la modélisation
- Métriques : F1 par classe et rappel, jamais l'accuracy seule.
- Découpage train/test stratifié pour conserver les classes rares des deux côtés.
- Regroupement des attaques en familles, en plus d'une classification binaire.

## Signatures observées
_À compléter après lecture de `reports/figures/class_signatures.png`._