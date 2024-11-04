from ...utils.api_client import BaseAuthorizedAPIClient
from .models import LumisectionHistogram2D, LumisectionHistogram2DFilters, PaginatedLumisectionHistogram2DList


class LumisectionHistogram2DClient(BaseAuthorizedAPIClient):
    data_model = LumisectionHistogram2D
    pagination_model = PaginatedLumisectionHistogram2DList
    filter_class = LumisectionHistogram2DFilters
    lookup_url = "th2/"

    def get(self, dataset_id: int, run_number: int, ls_number: int, me_id: int, **kwargs):
        edp = f"{dataset_id}/{run_number}/{ls_number}/{me_id}/"
        return super().get(edp, **kwargs)
