from importlib import util as importlib_util
from traceback import format_exc
from typing import Optional
from urllib.parse import parse_qs, urlparse
from warnings import warn

import requests
from requests import Response, Session
from requests.adapters import DEFAULT_RETRIES, HTTPAdapter
from requests.exceptions import HTTPError

from ..auth._base import BaseCredentials
from ..utils.logger import logger


if importlib_util.find_spec("tqdm"):
    from tqdm.auto import tqdm

    TQDM_INSTALLED = True
else:
    TQDM_INSTALLED = False


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

    @classmethod
    def _requests_get_retriable(cls, *args, retries=DEFAULT_RETRIES, **kwargs) -> Response:
        """
        requests.get() with an additional `retries` parameter.

        Specify retries=<number of attempts - 1> for simple use cases.
        For advanced usage, see https://docs.python-requests.org/en/latest/user/advanced/
        """
        with Session() as s:
            s.mount(cls.PRODUCTION_BASE_URL, HTTPAdapter(max_retries=retries))
            ret = s.get(*args, **kwargs)
        return ret

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

    def list(self, filters=None, retries=DEFAULT_RETRIES):
        filters = filters or self.filter_class()
        endpoint_url = self.api_url + self.lookup_url
        headers = self._build_headers()
        response = self._requests_get_retriable(
            endpoint_url,
            headers=headers,
            params=filters.cleandict(),
            timeout=self.default_timeout,
            retries=retries,
        )

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

    def __list_sync(
        self,
        filters,
        max_pages: Optional[int] = None,
        enable_progress: bool = False,
        retries=DEFAULT_RETRIES,
        keep_failed: bool = False,
        resume_from=None,
    ):
        next_string: Optional[str] = None
        results = []
        is_last_page = False

        if resume_from is not None:
            results = resume_from.results
            next_string = resume_from.next
            if next_string is None and len(results):
                warn(
                    "resume_from.next is None while resume_from.result is not empty, doing nothing.",
                    RuntimeWarning,
                    stacklevel=2,
                )
                is_last_page = True

        total_pages = 0
        use_tqdm = TQDM_INSTALLED and enable_progress

        if use_tqdm:
            progress = tqdm(desc="Progress", total=1)

        while is_last_page is False:
            next_token = parse_qs(urlparse(next_string).query).get("next_token") if next_string else None
            curr_filters = self.filter_class(**filters.dict())
            curr_filters.next_token = next_token
            try:
                response = self.list(curr_filters, retries=retries)
            except Exception as e:  # noqa: BLE001
                if use_tqdm:
                    progress.close()

                if not keep_failed:
                    raise e
                warn(
                    "HTTP request failed, returning partial results. Exception: " + format_exc(),
                    RuntimeWarning,
                    stacklevel=2,
                )
                return self.pagination_model(
                    next=next_string,
                    previous=None,
                    results=results,
                    exception=e,
                )
            results.extend(response.results)
            next_string = response.next
            is_last_page = next_string is None
            total_pages += 1
            max_pages_reached = max_pages and total_pages >= max_pages
            if use_tqdm:
                if is_last_page or max_pages_reached:
                    progress.update()
                else:
                    progress.total = total_pages + 1
                    progress.update(1)
            if max_pages_reached:
                break

        if use_tqdm:
            progress.close()

        return self.pagination_model(
            next=None,
            previous=None,
            results=results,  # No problem re-using last response count
        )

    def list_all(self, filters, max_pages: Optional[int] = None, **kwargs):
        if self.pagination_model is None:
            return self.list(filters)
        return self.__list_sync(filters, max_pages, **kwargs)
