import requests
from requests.exceptions import HTTPError

from ...utils.api_client import BaseAuthorizedAPIClient
from ...utils.logger import logger
from .models import FileIndex, FileIndexFilters, PaginatedFileIndexList


class FileIndexClient(BaseAuthorizedAPIClient):
    data_model = FileIndex
    pagination_model = PaginatedFileIndexList
    filter_class = FileIndexFilters
    lookup_url = "file-index/"

    def get(self, dataset_id: int, file_id: int):
        endpoint_url = f"{self.api_url}{self.lookup_url}{dataset_id}/{file_id}/"
        headers = self._build_headers()
        response = requests.get(endpoint_url, headers=headers, timeout=self.default_timeout)

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        return self.data_model(**response)
