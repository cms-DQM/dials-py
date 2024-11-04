from ...utils.api_client import BaseAuthorizedAPIClient
from .models import Lumisection, LumisectionFilters, PaginatedLumisectionList


class LumisectionClient(BaseAuthorizedAPIClient):
    data_model = Lumisection
    pagination_model = PaginatedLumisectionList
    filter_class = LumisectionFilters
    lookup_url = "lumisection/"

    def get(self, dataset_id: int, run_number: int, ls_number: int, **kwargs):
        edp = f"{dataset_id}/{run_number}/{ls_number}/"
        return super().get(edp, **kwargs)
