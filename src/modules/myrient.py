#!/usr/bin/python3

from typing import List
from bs4 import BeautifulSoup, NavigableString
from modules.core import ConsoleType, ContentResponse, Game, HttpContent, Source


class MyrientGame(Game):
    """
    implementation of Game class for Myrient site
    """


class MyrientSource(Source):
    """
    implementation of Source class for Myrient site
    """

    content: BeautifulSoup

    def __init__(self, console_type: ConsoleType, domain: str):
        super().__init__(console_type, domain)

    def fetch_content_url(self) -> ContentResponse:
        http_content_response = HttpContent(self.value).fetch_url_content()

        if http_content_response.is_failure():
            raise RuntimeError(
                f"Failure to obtain response content. Status Code: {http_content_response.status_code}, Message: {http_content_response.content}"
            )

        html_content = http_content_response.content
        self.content = BeautifulSoup(html_content, features="html.parser")
        return http_content_response

    def parse(self) -> List[Game]:
        table = self.content.find("table", attrs={"id": "list"})

        if table is None:
            raise RuntimeError("Could not find table in provided content.")
        elif isinstance(table, NavigableString):
            raise RuntimeError("Cannot traverse instance of NavigatableString.")

        parsed_table_rows: List[Game] = []
        for index, table_row in enumerate(table.find_all("tr")):
            # skip headers and file traversal row
            if index == 0 or index == 1:
                continue
            elif table_row is None:
                continue

            # TODO: implement a class to hold a generic class for parsing
            # parsed_table_rows.append()

        return parsed_table_rows
