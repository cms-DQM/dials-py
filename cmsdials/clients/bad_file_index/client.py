from ...utils.api_client import BaseAuthorizedAPIClient
from .models import BadFileIndex, BadFileIndexFilters, PaginatedBadFileIndexList


class BadFileIndexClient(BaseAuthorizedAPIClient):
    data_model = BadFileIndex
    pagination_model = PaginatedBadFileIndexList
    filter_class = BadFileIndexFilters
    lookup_url = "bad-file-index/"
