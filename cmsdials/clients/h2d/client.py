import requests
from requests.exceptions import HTTPError

from ...utils.api_client import BaseAuthorizedAPIClient
from ...utils.logger import logger
from .models import LumisectionHistogram2D, LumisectionHistogram2DFilters, PaginatedLumisectionHistogram2DList


class LumisectionHistogram2DClient(BaseAuthorizedAPIClient):
    data_model = LumisectionHistogram2D
    pagination_model = PaginatedLumisectionHistogram2DList
    filter_class = LumisectionHistogram2DFilters
    lookup_url = "th2/"

    def get(self, dataset_id: int, run_number: int, ls_number: int, me_id: int):
        endpoint_url = f"{self.api_url}{self.lookup_url}{dataset_id}/{run_number}/{ls_number}/{me_id}/"
        headers = self._build_headers()
        response = requests.get(endpoint_url, headers=headers, timeout=self.default_timeout)

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        return self.data_model(**response)
