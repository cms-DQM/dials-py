from ...utils.api_client import BaseAuthorizedAPIClient
from .models import LumisectionHistogram1D, LumisectionHistogram1DFilters, PaginatedLumisectionHistogram1DList


class LumisectionHistogram1DClient(BaseAuthorizedAPIClient):
    data_model = LumisectionHistogram1D
    pagination_model = LumisectionHistogram1DFilters
    filter_class = PaginatedLumisectionHistogram1DList
    lookup_url = "lumisection-h1d/"
