from netsentinel.features.splitting import StratifiedSplitter


def _sample(spark):
    rows = [(i, "A") for i in range(10)] + [(i, "B") for i in range(10, 20)]
    return spark.createDataFrame(rows, ["id", "family"])


def test_split_keeps_class_proportions_and_is_disjoint(spark) -> None:
    train, test = StratifiedSplitter("family", 0.8, 42).split(_sample(spark))

    assert train.filter("family = 'A'").count() == 8
    assert train.filter("family = 'B'").count() == 8
    assert test.filter("family = 'A'").count() == 2
    assert test.filter("family = 'B'").count() == 2

    train_ids = {row.id for row in train.collect()}
    test_ids = {row.id for row in test.collect()}
    assert train_ids.isdisjoint(test_ids)
    assert len(train_ids) + len(test_ids) == 20


def test_split_is_reproducible(spark) -> None:
    splitter = StratifiedSplitter("family", 0.8, 42)

    first = {row.id for row in splitter.split(_sample(spark))[0].collect()}
    second = {row.id for row in splitter.split(_sample(spark))[0].collect()}

    assert first == second