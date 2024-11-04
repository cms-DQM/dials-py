from ...utils.api_client import BaseAuthorizedAPIClient
from .models import FileIndex, FileIndexFilters, PaginatedFileIndexList


class FileIndexClient(BaseAuthorizedAPIClient):
    data_model = FileIndex
    pagination_model = PaginatedFileIndexList
    filter_class = FileIndexFilters
    lookup_url = "file-index/"

    def get(self, dataset_id: int, file_id: int, **kwargs):
        edp = f"{dataset_id}/{file_id}/"
        return super().get(edp, **kwargs)
