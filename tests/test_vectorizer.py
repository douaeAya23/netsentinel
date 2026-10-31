import pytest

from netsentinel.features.vectorizer import build_vector_pipeline


def test_vector_pipeline_standardizes_features(spark) -> None:
    df = spark.createDataFrame([(1.0, 10.0), (2.0, 20.0), (3.0, 30.0)], ["a", "b"])

    model = build_vector_pipeline(["a", "b"]).fit(df)
    rows = model.transform(df).orderBy("a").collect()

    assert len(rows[0].features) == 2
    assert rows[0].features[0] == pytest.approx(-1.0)
    assert rows[1].features[0] == pytest.approx(0.0)
    assert rows[2].features[0] == pytest.approx(1.0)