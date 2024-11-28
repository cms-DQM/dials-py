from ...utils.api_client import BaseAuthorizedAPIClient
from .models import DatasetIndex, DatasetIndexFilters, PaginatedDatasetIndexList


class DatasetIndexClient(BaseAuthorizedAPIClient):
    data_model = DatasetIndex
    pagination_model = PaginatedDatasetIndexList
    filter_class = DatasetIndexFilters
    lookup_url = "dataset-index/"

    def get(self, dataset_id: int, file_id: int, **kwargs):
        edp = f"{dataset_id}/{file_id}/"
        return super().get(edp, **kwargs)
