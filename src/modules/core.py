#!/usr/bin/env python

from dataclasses import dataclass
from bs4 import Tag
from requests import get
from requests import HTTPError, ConnectionError, Timeout, RequestException
from requests_cache import CachedSession
from datetime import timedelta
from tenacity import retry, stop_after_attempt, wait_random, retry_if_exception_type
from urllib.parse import urlparse
from http import HTTPStatus
from os import path, makedirs, getenv
from typing import List
from dotenv import load_dotenv
from enum import Enum
from abc import ABC, abstractmethod
from modules.sources import MYRENT_DOMAINS

load_dotenv()

CACHE_PATH = getenv("CACHE_PATH") or ""


class ContentResponse:
    url: str = ""
    status_code: int = 0
    content: str = ""

    bad_requests: List[HTTPStatus] = [
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.GATEWAY_TIMEOUT,
        HTTPStatus.REQUEST_TIMEOUT,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ]

    def __init__(self, url: str, status_code: int, content: str):
        self.url = url
        self.status_code = status_code
        self.content = content

    def is_failure(self) -> bool:
        return self.status_code in self.bad_requests

    def is_success(self) -> bool:
        return self.status_code not in self.bad_requests


class HttpContent:
    url: str = ""

    headers = {
        "User Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }

    def __init__(self, url: str):
        self.url = url

    @property
    def cache_path(self) -> str:
        return path.join(CACHE_PATH, self.domain)

    @property
    def domain(self) -> str:
        parsed_url = urlparse(self.url)
        domain = parsed_url.netloc
        return domain

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random(min=1, max=2),
        retry=retry_if_exception_type(RequestException),
    )
    def download(self, file_path: str) -> ContentResponse:
        try:
            print(f"Requesting {self.url} and saving to {file_path}")
            response = get(self.url, stream=True)
            response.raise_for_status()
            makedirs(path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print(f"Successfully saved to {file_path}")
            return ContentResponse(self.url, HTTPStatus.OK, file_path)
        except RequestException as exception:
            # Provide default values if exception.response is None
            status_code = (
                exception.response.status_code
                if exception.response
                else HTTPStatus.INTERNAL_SERVER_ERROR
            )
            text = (
                exception.response.text
                if exception.response
                else "No response text available"
            )
            return ContentResponse(self.url, status_code, text)

    def fetch_url_content(self) -> ContentResponse:
        try:
            print(f"Making request to {self.url}.")
            cached_session = CachedSession(
                self.cache_path, expire_after=timedelta(hours=3)
            )
            response = cached_session.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            print(
                f"Received response for {self.url} with status code {response.status_code}."
            )
            return ContentResponse(self.url, response.status_code, response.text)
        except HTTPError as errh:
            return ContentResponse(
                self.url, errh.response.status_code, errh.response.text
            )
        except ConnectionError as connection_error:
            # Provide default values if exception.response is None
            status_code = (
                connection_error.response.status_code
                if connection_error.response is not None
                else HTTPStatus.BAD_GATEWAY
            )
            text = (
                connection_error.response.text
                if connection_error.response is not None
                else "No response text available"
            )
            return ContentResponse(self.url, status_code, text)
        except Timeout as connection_timeout:
            # Provide default values if exception.response is None
            status_code = (
                connection_timeout.response.status_code
                if connection_timeout.response is not None
                else HTTPStatus.GATEWAY_TIMEOUT
            )
            text = (
                connection_timeout.response.text
                if connection_timeout.response is not None
                else "No response text available"
            )
            return ContentResponse(self.url, status_code, text)
        except RequestException as request_error:
            # Provide default values if exception.response is None
            status_code = (
                request_error.response.status_code
                if request_error.response is not None
                else HTTPStatus.BAD_REQUEST
            )
            text = (
                request_error.response.text
                if request_error.response is not None
                else "No response text available"
            )
            return ContentResponse(self.url, status_code, text)


class ConsoleType(Enum):
    """
    enum for console types
    """

    UNKNOWN = 1
    PLAYSTATION_1 = 2
    PLAYSTATION_2 = 3
    PLAYSTATION_3 = 4
    PLAYSTATION_4 = 5
    PLAYSTATION_5 = 6
    GAMECUBE = 7
    GAMEBOY_ADVANCED = 8

    @staticmethod
    def from_string(console: str):
        console = console.lower().strip()
        if console in ["playstation_1", "playstation 1"]:
            return ConsoleType.PLAYSTATION_1
        elif console in "gamecube":
            return ConsoleType.GAMECUBE
        else:
            raise NotImplementedError(f"Unsupported console {console}.")


class Game(ABC):
    """
    abstract class for Game
    """

    content: Tag | str

    def __init__(self, content: Tag | str):
        self.content = content

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_link(self) -> str:
        pass

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass


class Source(ABC):
    """
    abstract class for Source
    """

    key: ConsoleType
    value: str

    def __init__(self, key: ConsoleType, value: str):
        self.key = key
        self.value = value

    @abstractmethod
    def fetch_content_url(self) -> ContentResponse:
        pass

    @abstractmethod
    def parse(self) -> List[Game]:
        pass


class Console(ABC):
    """
    abstract class for consoles
    """

    console_type: ConsoleType
    sources: List[Source]

    def __init__(self, console_type: ConsoleType):
        self.console_type = console_type

    def get_source_by_key_or_default(self, key: ConsoleType) -> Source | None:
        """
        function to get source by key or default
        """
        return next(
            (source for source in self.sources if source.key.value == key.value), None
        )

    def get_sources_by_key(self, key: ConsoleType) -> List[str]:
        """
        function to get a list of sources by key
        """
        return [
            source.value for source in self.sources if source.key.value == key.value
        ]

    def add_source(self, source: Source):
        """
        function to add a new source
        """
        existing_source = self.get_source_by_key_or_default(source.key)

        if existing_source is not None:
            raise RuntimeError(f"Entity already exists.")

        self.sources.append(source)

    def add_sources(self, sources: List[Source]):
        """
        function to add a list of sources
        """
        self.sources = list(set(self.sources + sources))

    def remove_source_by_key(self, key: ConsoleType):
        """
        function to remove a source by key
        """
        existing_source = self.get_source_by_key_or_default(key)

        if existing_source is None:
            return

        self.sources.remove(existing_source)


class ConsoleFactory:
    """
    factory class for creating console objects
    """

    console_type: ConsoleType

    def __init__(self, console_type: ConsoleType):
        self.console_type = console_type

    def create_console(self) -> Console:
        if self.console_type == ConsoleType.PLAYSTATION_1:
            return PlayStationOneConsole()
        else:
            raise NotImplementedError(f"Unsupported console {self.console_type}.")


class PlayStationOneConsole(Console):
    def __init__(self):
        super().__init__(ConsoleType.PLAYSTATION_1)


class PlayStationTwoConsole(Console):
    def __init__(self):
        super().__init__(ConsoleType.PLAYSTATION_1)


class GameCubeConsole(Console):
    def __init__(self):
        super().__init__(ConsoleType.GAMECUBE)
