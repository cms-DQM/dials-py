import requests

from ...utils.api_client import BaseAuthorizedAPIClient
from .models import ConfiguredMEs, Lumisection, LumisectionFilters, PaginatedLumisectionList


class LumisectionClient(BaseAuthorizedAPIClient):
    data_model = Lumisection
    pagination_model = PaginatedLumisectionList
    filter_class = LumisectionFilters
    lookup_url = "lumisection/"

    def configured_mes(self):
        endpoint_url = self.api_url + self.lookup_url + "configured-mes/"
        headers = {"accept": "application/json"}
        self.creds.before_request(headers)
        response = requests.get(endpoint_url, headers=headers)
        response.raise_for_status()
        response = response.json()
        return ConfiguredMEs(**response)
