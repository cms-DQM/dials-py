from cmsdials.filters import OMSFilter, OMSPage

from .utils import DEFAULT_TEST_WORKSPACE, setup_dials_object


def test_query_runs() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.oms.query(
        endpoint="runs", filters=[OMSFilter(attribute_name="run_number", value=382921, operator="EQ")]
    )
    assert isinstance(data, dict)
    assert data["meta"]["totalResourceCount"] == 1


def test_query_lumisections() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.oms.query(
        endpoint="lumisections",
        filters=[OMSFilter(attribute_name="run_number", value=382921, operator="EQ")],
        pages=[OMSPage(attribute_name="limit", value=5000)],
    )
    assert isinstance(data, dict)
    assert data["meta"]["totalResourceCount"] > 100


def test_query_datasetrates() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.oms.query(
        endpoint="datasetrates",
        filters=[
            OMSFilter(attribute_name="run_number", value=382921, operator="EQ"),
            OMSFilter(attribute_name="dataset_name", value="ZeroBias", operator="EQ"),
        ],
        pages=[OMSPage(attribute_name="limit", value=5000)],
    )
    assert isinstance(data, dict)
    assert data["meta"]["totalResourceCount"] > 100
