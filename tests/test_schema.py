from netsentinel.ingestion.schema import FEATURE_COLUMNS, build_flow_schema


def test_schema_has_78_features_plus_label() -> None:
    assert len(FEATURE_COLUMNS) == 78
    assert len(build_flow_schema().fields) == 79