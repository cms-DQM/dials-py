import requests
from requests.exceptions import HTTPError

from ...utils.api_client import BaseAuthorizedAPIClient
from ...utils.logger import logger
from .models import PaginatedRunList, Run, RunFilters


class RunClient(BaseAuthorizedAPIClient):
    data_model = Run
    pagination_model = PaginatedRunList
    filter_class = RunFilters
    lookup_url = "run/"

    def get(self, dataset_id: int, run_number: int):
        endpoint_url = f"{self.api_url}{self.lookup_url}{dataset_id}/{run_number}/"
        headers = self._build_headers()
        response = requests.get(endpoint_url, headers=headers)

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        return self.data_model(**response)
