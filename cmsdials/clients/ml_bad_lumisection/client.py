from ...utils.api_client import BaseAuthorizedAPIClient
from .models import MLBadLumisection, MLBadLumisectionFilters, PaginatedMLBadLumisectionList


class MLBadLumisectionClient(BaseAuthorizedAPIClient):
    data_model = MLBadLumisection
    pagination_model = PaginatedMLBadLumisectionList
    filter_class = MLBadLumisectionFilters
    lookup_url = "ml-bad-lumisection/"

    def get(self, model_id: int, dataset_id: int, run_number: int, ls_number: int, me_id: int, **kwargs):
        edp = f"{model_id}/{dataset_id}/{run_number}/{ls_number}/{me_id}/"
        return super().get(edp, **kwargs)

    def cert_json(self, model_id__in: list[int], dataset_id__in: list[int], run_number__in: list[int], **kwargs):
        edp = "cert-json/"
        midin = ",".join(str(v) for v in model_id__in)
        didin = ",".join(str(v) for v in dataset_id__in)
        ridin = ",".join(str(v) for v in run_number__in)
        params = {"model_id__in": midin, "dataset_id__in": didin, "run_number__in": ridin}
        return super().get(edp, params=params, return_raw_json=True, **kwargs)

    def golden_json(self, model_id__in: list[int], dataset_id__in: list[int], run_number__in: list[int], **kwargs):
        edp = "golden-json/"
        midin = ",".join(str(v) for v in model_id__in)
        didin = ",".join(str(v) for v in dataset_id__in)
        ridin = ",".join(str(v) for v in run_number__in)
        params = {"model_id__in": midin, "dataset_id__in": didin, "run_number__in": ridin}
        return super().get(edp, params=params, return_raw_json=True, **kwargs)
