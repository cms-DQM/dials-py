import requests
from requests.exceptions import HTTPError

from ...utils.api_client import BaseAuthorizedAPIClient
from ...utils.logger import logger
from .models import Lumisection, LumisectionFilters, PaginatedLumisectionList


class LumisectionClient(BaseAuthorizedAPIClient):
    data_model = Lumisection
    pagination_model = PaginatedLumisectionList
    filter_class = LumisectionFilters
    lookup_url = "lumisection/"

    def get(self, dataset_id: int, run_number: int, ls_number: int):
        endpoint_url = f"{self.api_url}{self.lookup_url}{dataset_id}/{run_number}/{ls_number}/"
        headers = self._build_headers()
        response = requests.get(endpoint_url, headers=headers)

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        return self.data_model(**response)
