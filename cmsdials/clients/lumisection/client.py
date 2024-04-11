from ...utils.api_client import BaseAuthorizedAPIClient
from .models import Lumisection, LumisectionFilters, PaginatedLumisectionList


class LumisectionClient(BaseAuthorizedAPIClient):
    data_model = Lumisection
    pagination_model = PaginatedLumisectionList
    filter_class = LumisectionFilters
    lookup_url = "lumisection/"
