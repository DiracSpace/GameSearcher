#!/usr/bin/env python

from bs4 import Tag

from os import path, makedirs, getenv
from typing import List
from dotenv import load_dotenv
from enum import Enum
from abc import ABC, abstractmethod

load_dotenv()

SAVE_PATH = getenv("SAVE_PATH")


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

    content: Tag

    def __init__(self, content: Tag):
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
    save_path: str | None

    def __init__(self, key: ConsoleType, value: str):
        self.key = key
        self.value = value
        self.save_path = SAVE_PATH

    @abstractmethod
    def fetch_content_url(self) -> ContentResponse:
        pass

    @abstractmethod
    def parse(self) -> List[Game]:
        pass

    @abstractmethod
    def download(self, link: str, file_name: str) -> str:
        pass


class Console(ABC):
    """
    abstract class for consoles
    """

    console_type: ConsoleType
    sources: List[Source]

    def __init__(self, console_type: ConsoleType):
        self.console_type = console_type

    @property
    def has_multiple_sources(self) -> bool:
        return len(self.sources) > 1

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
