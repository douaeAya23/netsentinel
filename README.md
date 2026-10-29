# NetSentinel

Détection d'intrusions réseau à grande échelle avec **PySpark** et **Spark MLlib**,
sur le dataset réel **CIC-IDS2017** (environ 2,8 M de flux réseau labellisés).

> Projet en cours de construction.

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
make install
make test
```

## Prérequis

Python 3.10+ et Java 17 (nécessaire à Spark).