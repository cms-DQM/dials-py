from ...utils.api_client import BaseAuthorizedAPIClient
from .models import LumisectionHistogram1D, LumisectionHistogram1DFilters, PaginatedLumisectionHistogram1DList


class LumisectionHistogram1DClient(BaseAuthorizedAPIClient):
    data_model = LumisectionHistogram1D
    pagination_model = PaginatedLumisectionHistogram1DList
    filter_class = LumisectionHistogram1DFilters
    lookup_url = "th1/"
