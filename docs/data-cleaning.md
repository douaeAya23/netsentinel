# Choix de nettoyage

| Étape | Pourquoi |
|---|---|
| Schéma explicite | Spark infère mal les types sur de gros volumes, et le schéma documente le dataset |
| Noms en snake_case | Les noms d'origine contiennent des espaces, des `/` et un doublon (`Fwd Header Length`), ce qui complique les requêtes Spark |
| Labels normalisés | Les labels « Web Attack » contiennent un caractère mal encodé |
| `Infinity` / NaN → null | `Flow Bytes/s` et `Flow Packets/s` contiennent des valeurs infinies (division par une durée nulle), inutilisables par les modèles |
| Lignes nulles supprimées | MLlib refuse les valeurs manquantes dans les vecteurs de features |
| Doublons supprimés | Évite de fausser l'entraînement et la mesure de performance (fuite entre train et test) |
| Parquet | Format colonnaire compressé, bien plus rapide à relire que le CSV |

## Limites

Le dataset a été capturé dans un banc d'essai contrôlé, et des travaux publiés
y ont relevé des défauts d'étiquetage. Les chiffres avant/après nettoyage sont
consignés ci-dessous.

- Lignes brutes : _à compléter_
- Lignes après nettoyage : _à compléter_