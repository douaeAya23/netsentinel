from netsentinel.features.labels import FAMILIES
from netsentinel.modeling.factories import LogisticRegressionFactory, RandomForestFactory
from netsentinel.modeling.tasks import BINARY_TASK, FAMILY_TASK


def test_family_task_excludes_rare_and_keeps_contiguous_indices() -> None:
    assert FAMILIES[-1] == "Rare"
    assert "Rare" not in FAMILY_TASK.class_names
    assert FAMILY_TASK.class_names == FAMILIES[:-1]
    assert BINARY_TASK.class_names == ("BENIGN", "ATTACK")


def test_factories_apply_their_hyperparameters(spark) -> None:
    logistic = LogisticRegressionFactory(max_iter=7).create("label")
    forest = RandomForestFactory(num_trees=5, max_depth=3, seed=1).create("label")

    assert logistic.getMaxIter() == 7
    assert forest.getNumTrees() == 5
    assert forest.getMaxDepth() == 3