from concurrent.futures import ThreadPoolExecutor
from math import ceil
from typing import Optional

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

    def __init__(self, creds: BaseCredentials, nthreads: Optional[int] = None, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        self.creds = creds
        self.nthreads = nthreads or 1

    def get(self, id: str):
        endpoint_url = self.api_url + self.lookup_url + str(id) + "/"
        headers = {"accept": "application/json"}
        self.creds.before_request(headers)
        response = requests.get(endpoint_url, headers=headers)

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
        headers = {"accept": "application/json"}
        self.creds.before_request(headers)
        response = requests.get(endpoint_url, headers=headers, params=filters.cleandict())

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.info(f"Api raw response: {response.text}")
            raise err

        response = response.json()
        return self.pagination_model(**response)

    def __list_sync(self, filters, max_pages: Optional[int] = None):
        page = 1
        results = []
        is_last_page = False

        while is_last_page is False:
            curr_filters = self.filter_class(**filters.dict())
            curr_filters.page = str(page)
            response = self.list(curr_filters)
            results.extend(response.results)
            is_last_page = response.next is None
            page += 1
            if max_pages and page > max_pages:
                break

        return self.pagination_model(
            count=response.count, next=None, previous=None, results=results  # No problem re-using last response count
        )

    def __list_multithreaded(self, filters, max_pages: Optional[int] = None):
        results = []

        # Request the first page to compute number of pages
        curr_filters = self.filter_class(**filters.dict())
        curr_filters.page = "1"
        response = self.list(curr_filters)
        results.extend(response.results)
        count = response.count
        n_pages = ceil(response.count / 10)
        n_pages = max_pages if max_pages is not None and n_pages > max_pages else n_pages

        # If there isn't another page, just return current results
        if response.next is None:
            return response

        # Request other pages
        all_filters = [{**filters.dict(), "page": str(page)} for page in range(2, n_pages + 1)]
        all_filters = [self.filter_class(**filter) for filter in all_filters]
        with ThreadPoolExecutor(max_workers=self.nthreads) as executor:
            jobs = executor.map(self.list, all_filters)
            del all_filters
            [results.extend(job_result.results) for job_result in jobs]
            del jobs

        return self.pagination_model(count=count, next=None, previous=None, results=results)

    def list_all(self, filters, max_pages: Optional[int] = None):
        return (
            self.__list_sync(filters, max_pages)
            if self.nthreads is None
            else self.__list_multithreaded(filters, max_pages)
        )
