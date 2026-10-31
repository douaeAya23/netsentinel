# %% [markdown]
# # EDA : CIC-IDS2017 nettoyé
# Ce notebook ne contient aucune logique métier : il appelle `netsentinel.eda`
# et sert à lire et interpréter les résultats. Prérequis : `make prepare`.

# %%
from pathlib import Path

from IPython.display import Image, display

from netsentinel.config import load_config
from netsentinel.eda.key_features import KEY_FEATURE_DESCRIPTIONS, KEY_FEATURES
from netsentinel.eda.statistics import class_distribution, median_by_class
from netsentinel.spark_session import build_spark_session
from netsentinel.storage import ParquetStore

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
config = load_config(ROOT / "configs/config.yaml")
spark = build_spark_session(config.spark)
df = ParquetStore().read(spark, ROOT / config.paths.processed_dir / "flows").cache()
print(f"{df.count():,} flux, {len(df.columns)} colonnes")

# %% [markdown]
# ## 1. Déséquilibre des classes
# Le trafic bénin domine, certaines attaques sont rarissimes. Conséquence directe :
# l'accuracy est trompeuse, on évaluera avec le F1 par classe.

# %%
distribution = class_distribution(df)
distribution

# %%
display(Image(ROOT / config.paths.reports_dir / "figures/class_distribution.png"))

# %% [markdown]
# ## 2. Signature de chaque attaque
# Pourquoi ces features ? Voir leur description ci-dessous.

# %%
for name, description in KEY_FEATURE_DESCRIPTIONS.items():
    print(f"{name:32s} {description}")

# %%
median_by_class(df, KEY_FEATURES)

# %%
display(Image(ROOT / config.paths.reports_dir / "figures/class_signatures.png"))

# %% [markdown]
# ## 3. Corrélations
# Des features très corrélées sont redondantes : on pourra en retirer pour
# alléger les modèles.

# %%
display(Image(ROOT / config.paths.reports_dir / "figures/correlation_heatmap.png"))

# %%
spark.stop()