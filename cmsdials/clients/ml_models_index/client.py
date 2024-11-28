from ...utils.api_client import BaseAuthorizedAPIClient
from .models import MLModelsIndex, MLModelsIndexFilters, PaginatedMLModelsIndexList


class MLModelsIndexClient(BaseAuthorizedAPIClient):
    data_model = MLModelsIndex
    pagination_model = PaginatedMLModelsIndexList
    filter_class = MLModelsIndexFilters
    lookup_url = "ml-models-index/"

    def get(self, model_id: int, **kwargs):
        edp = f"{model_id}/"
        return super().get(edp, **kwargs)
