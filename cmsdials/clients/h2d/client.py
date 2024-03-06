from ...utils.api_client import BaseAuthorizedAPIClient
from .models import LumisectionHistogram2D, LumisectionHistogram2DFilters, PaginatedLumisectionHistogram2DList


class LumisectionHistogram2DClient(BaseAuthorizedAPIClient):
    data_model = LumisectionHistogram2D
    pagination_model = LumisectionHistogram2DFilters
    filter_class = PaginatedLumisectionHistogram2DList
    lookup_url = "lumisection-h2d/"
