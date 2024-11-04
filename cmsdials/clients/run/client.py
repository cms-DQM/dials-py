from ...utils.api_client import BaseAuthorizedAPIClient
from .models import PaginatedRunList, Run, RunFilters


class RunClient(BaseAuthorizedAPIClient):
    data_model = Run
    pagination_model = PaginatedRunList
    filter_class = RunFilters
    lookup_url = "run/"

    def get(self, dataset_id: int, run_number: int, **kwargs):
        edp = f"{dataset_id}/{run_number}/"
        return super().get(edp, **kwargs)
