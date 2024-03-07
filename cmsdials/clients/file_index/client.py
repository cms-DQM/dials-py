from ...utils.api_client import BaseAuthorizedAPIClient
from .models import FileIndex, FileIndexFilters, PaginatedFileIndexList


class FileIndexClient(BaseAuthorizedAPIClient):
    data_model = FileIndex
    pagination_model = PaginatedFileIndexList
    filter_class = FileIndexFilters
    lookup_url = "file-index/"
