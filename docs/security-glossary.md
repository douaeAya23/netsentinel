# Glossaire de sécurité

Définitions générales, reliées à ce que ce projet a mesuré. Les outils exacts
utilisés pour générer les attaques sont décrits sur la page officielle du dataset
(Canadian Institute for Cybersecurity, Université du Nouveau-Brunswick).

## Notions de base

| Terme | Définition |
|---|---|
| **Flux réseau (flow)** | Ensemble des paquets d'une même conversation entre deux machines. Une ligne du dataset = un flux, décrit par 78 statistiques (durée, nombre de paquets, débits, drapeaux TCP...) |
| **IDS** | *Intrusion Detection System* : système qui repère des activités malveillantes. Il alerte, alors qu'un IPS bloque en plus |
| **Faux négatif** | Une attaque non détectée : l'erreur la plus coûteuse en sécurité. Elle correspond au **rappel** |
| **Faux positif** | Une fausse alerte. Trop de fausses alertes épuisent les analystes. Elles correspondent à la **précision** |
| **Banc d'essai** | Environnement contrôlé où les attaques sont déclenchées volontairement. Le trafic est réel, mais plus simple que celui d'un vrai réseau d'entreprise |

## Drapeaux TCP (features `*_flag_count`)

| Drapeau | Rôle |
|---|---|
| **SYN** | Demande d'ouverture d'une connexion |
| **ACK** | Accusé de réception |
| **PSH** | Demande d'envoyer immédiatement les données à l'application |
| **FIN** | Fermeture normale de la connexion |
| **RST** | Coupure brutale de la connexion |
| **URG** | Données urgentes |

## Les attaques du dataset

| Famille | Attaque | Principe | Ce que le projet a observé |
|---|---|---|---|
| **PortScan** | Scan de ports | L'attaquant sonde de nombreux ports pour découvrir les services ouverts, première étape d'une intrusion | Signature la plus nette : durée médiane de 50 µs, 1 paquet par sens, 40 000 paquets/s. F1 de 0,994 |
| **DoS** | Hulk, GoldenEye | Inondation de requêtes HTTP pour saturer un serveur depuis une machine | Flux longs mais de très faible débit : l'attaque se voit au *nombre* de flux, pas à leur débit |
| **DoS** | slowloris, Slowhttptest | Attaque *lente* : on garde un maximum de connexions ouvertes avec très peu de données, jusqu'à épuiser les connexions du serveur | Flux de 63 à 100 s, paquets quasi vides, 6 à 10 s entre deux paquets |
| **DDoS** | DDoS | Même objectif qu'un DoS, depuis de nombreuses machines à la fois, donc plus difficile à bloquer | Flux courts de 4 paquets par sens. F1 de 0,999 |
| **BruteForce** | FTP-Patator, SSH-Patator | Essai répété de mots de passe sur un service FTP (transfert de fichiers) ou SSH (accès distant) | Flux de 24 (FTP) et 53 (SSH) paquets sur 9 à 12 s. F1 de 0,983 |
| **WebAttack** | Brute Force, XSS, SQL injection | Brute force sur un formulaire de connexion web ; **XSS** : injecter un script exécuté dans le navigateur d'autres utilisateurs ; **SQL injection** : injecter des commandes dans la base de données du site | Quasi identiques entre elles dans ces features, car le contenu HTTP n'est pas visible. Rappel de 0,886 |
| **Bot** | Botnet | Machine infectée, pilotée à distance par un serveur de commande et de contrôle | Classe la plus difficile (F1 de 0,58) : trafic discret de quelques paquets |
| **Rare** | Infiltration, Heartbleed | **Infiltration** : intrusion déjà réalisée, l'attaquant explore le réseau depuis l'intérieur. **Heartbleed** : faille du chiffrement OpenSSL (2014) qui permet de lire la mémoire d'un serveur | Moins de 50 flux : trop peu pour une évaluation fiable. Exclue de l'évaluation multi-classes |

## Pourquoi un flux ne dit pas tout

Les features décrivent la *forme* d'une conversation (durée, volumes, rythme), pas son
*contenu*. Un XSS et un trafic web légitime peuvent avoir la même forme, ce qui
limite ce type de détection aux attaques qui ont une signature statistique.
Détecter un botnet demande aussi de suivre une machine dans le temps (périodicité
de ses connexions), ce que ce fichier ne permet pas : il ne contient ni adresse IP
ni horodatage.