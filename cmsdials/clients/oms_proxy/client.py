from typing import Optional

import requests
from requests.exceptions import HTTPError

from ...auth._base import BaseCredentials
from ...utils.api_client import BaseAPIClient
from ...utils.logger import logger
from .models import OMSFilter, OMSPage


class OMSProxyClient(BaseAPIClient):
    default_timeout = 30
    lookup_url = "oms-proxy/"

    def __init__(
        self,
        creds: BaseCredentials,
        *args: str,
        **kwargs: str,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.creds = creds

    def _build_headers(self) -> dict:
        base = {"accept": "application/json"}
        self.creds.before_request(base)
        return base

    def query(self, endpoint: str, filters: list[OMSFilter], pages: Optional[list[OMSPage]] = None):
        headers = self._build_headers()
        endpoint_url = self.api_url + self.lookup_url

        # Format filters
        filters = {f"filter[{_filter.attribute_name}][{_filter.operator}]": _filter.value for _filter in filters}
        pages = {f"page[{page.attribute_name}]": page.value for page in pages} if pages and len(pages) > 0 else {}
        params = {"endpoint": endpoint, **filters, **pages}

        response = requests.get(endpoint_url, headers=headers, params=params, timeout=self.default_timeout)
        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        return response.json()
