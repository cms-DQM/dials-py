import requests
from requests.exceptions import HTTPError

from ...utils.api_client import BaseAuthorizedAPIClient
from ...utils.logger import logger
from .models import LumisectionHistogram1D, LumisectionHistogram1DFilters, PaginatedLumisectionHistogram1DList


class LumisectionHistogram1DClient(BaseAuthorizedAPIClient):
    data_model = LumisectionHistogram1D
    pagination_model = PaginatedLumisectionHistogram1DList
    filter_class = LumisectionHistogram1DFilters
    lookup_url = "th1/"

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
