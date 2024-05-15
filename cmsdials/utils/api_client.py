from typing import Optional
from urllib.parse import parse_qs, urlparse

import requests
from requests.exceptions import HTTPError

from ..auth._base import BaseCredentials
from ..utils.logger import logger


class BaseAPIClient:
    PRODUCTION_BASE_URL = "https://cmsdials-api.web.cern.ch/"
    PRODUCTION_API_ROUTE = "api/"
    PRODUCTION_API_VERSION = "v1/"

    def __init__(
        self, base_url: Optional[str] = None, route: Optional[str] = None, version: Optional[str] = None
    ) -> None:
        self.base_url = self.__endswithslash(base_url or self.PRODUCTION_BASE_URL)
        self.route = self.__endswithslash(route or self.PRODUCTION_API_ROUTE)
        self.version = self.__endswithslash(version or self.PRODUCTION_API_VERSION)

    @staticmethod
    def __endswithslash(value: str) -> str:
        if value.endswith("/") is False:
            return value + "/"
        return value

    @property
    def api_url(self):
        return self.base_url + self.route + self.version


class BaseAuthorizedAPIClient(BaseAPIClient):
    data_model = None
    pagination_model = None
    filter_class = None
    lookup_url = None
    default_timeout = 30  # seconds

    def __init__(
        self,
        creds: BaseCredentials,
        workspace: Optional[str] = None,
        *args: str,
        **kwargs: str,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.creds = creds
        self.workspace = workspace

    def _build_headers(self) -> dict:
        base = {"accept": "application/json"}
        if self.workspace is not None:
            base["Workspace"] = self.workspace
        self.creds.before_request(base)
        return base

    def get(self, id: int):  # noqa: A002
        endpoint_url = self.api_url + self.lookup_url + str(id) + "/"
        headers = self._build_headers()
        response = requests.get(endpoint_url, headers=headers, timeout=self.default_timeout)

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        return self.data_model(**response)

    def list(self, filters=None):
        filters = filters or self.filter_class()
        endpoint_url = self.api_url + self.lookup_url
        headers = self._build_headers()
        response = requests.get(endpoint_url, headers=headers, params=filters.cleandict(), timeout=self.default_timeout)

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        if self.pagination_model:
            return self.pagination_model(**response)
        elif isinstance(response, list):
            return [self.data_model(**res) for res in response]

        raise ValueError("pagination model is None and response is not a list.")

    def __list_sync(self, filters, max_pages: Optional[int] = None):
        next_token = None
        results = []
        is_last_page = False
        total_pages = 0

        while is_last_page is False:
            curr_filters = self.filter_class(**filters.dict())
            curr_filters.next_token = next_token
            response = self.list(curr_filters)
            results.extend(response.results)
            is_last_page = response.next is None
            next_token = parse_qs(urlparse(response.next).query).get("next_token") if response.next else None
            total_pages += 1
            if max_pages and total_pages > max_pages:
                break

        return self.pagination_model(
            next=None,
            previous=None,
            results=results,  # No problem re-using last response count
        )

    def list_all(self, filters, max_pages: Optional[int] = None):
        if self.pagination_model is None:
            return self.list(filters)
        return self.__list_sync(filters, max_pages)
