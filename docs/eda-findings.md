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

## Signatures observées (médiane par classe, features clés)
- **Trafic bénin** : flux courts (40 ms), 2 paquets dans chaque sens, environ
  60 octets par paquet, soit des échanges de type requête/réponse brefs.
- **PortScan** : signature la plus nette, 50 µs de durée médiane, 1 paquet dans
  chaque sens, 40 000 paquets/s.
- **DoS par inondation (Hulk, GoldenEye)** : flux longs (86 s et 12 s) avec un
  débit par flux très faible (moins de 1 paquet/s). L'attaque se voit au nombre
  de flux, pas au débit d'un flux, ce que des features par flux ne capturent pas.
- **DoS lents (slowloris, Slowhttptest)** : 100 s et 63 s, paquets quasi vides,
  6 à 10 s entre deux paquets : connexions maintenues ouvertes à très bas débit.
- **DDoS** : 1,9 s, 4 paquets dans chaque sens, environ 830 octets par paquet.
  Proche de Hulk par la taille des paquets, plus court.
- **Brute force FTP/SSH** : flux de 24 et 53 paquets sur 9 à 12 s.
- **Web attacks** : Brute Force et XSS quasi identiques (environ 5,5 s,
  3 paquets, 0 octet) : le contenu HTTP n'est pas visible dans ces features.
- **Heartbleed** : flux de 119 s avec environ 2 800 paquets envoyés, valeurs très
  au-dessus des autres classes, mais seulement 11 flux.

## Points de vigilance
- `init_win_bytes_forward` et `psh_flag_count` séparent les classes d'une façon qui
  semble liée à l'outil ou au système de l'émetteur plutôt qu'au comportement
  (29 200 pour neuf classes d'attaque, 122 pour le trafic bénin). Test prévu :
  entraîner avec et sans ces features.
- Trois paires de features sont quasi redondantes (paquets avant/arrière,
  taille moyenne des paquets, débits de paquets) : filtre de corrélation prévu.
- Les classes rares (Heartbleed, Infiltration) correspondent peut-être à une seule
  session d'attaque : risque de fuite entre entraînement et test.
- Les médianes ne disent rien de la régularité ni du volume agrégé d'une attaque.