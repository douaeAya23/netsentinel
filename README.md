# NetSentinel

Détection d'intrusions réseau à grande échelle avec **PySpark** et **Spark MLlib**,
sur le dataset réel **CIC-IDS2017** (environ 2,8 M de flux réseau labellisés).

## Préparation des données

Télécharge CIC-IDS2017 (version `MachineLearningCSV`) dans `data/raw/`, puis :

```bash
make prepare
```

Le job ingère les CSV avec un schéma explicite, nettoie les données (voir
[docs/data-cleaning.md](docs/data-cleaning.md)) et écrit du Parquet dans `data/processed/flows`.

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
make install
pip install -e ".[notebook]"   # optionnel : pour exécuter le notebook d'EDA
make test
```

## Prérequis

Python 3.10+ et Java 17 (nécessaire à Spark).