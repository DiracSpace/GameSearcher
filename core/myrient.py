#!/usr/bin/python3

from os import path
from re import sub
from typing import List
from urllib.parse import unquote, urljoin
from bs4 import BeautifulSoup, NavigableString
from modules.core import ConsoleType, ContentResponse, Game, HttpContent, Source


class MyrientGame(Game):
    """
    implementation of Game class for Myrient site
    """

    def get_title(self) -> str:
        table_row_link_data_cell = self.content.find("td")

        if table_row_link_data_cell is None:
            raise RuntimeError("Could not find table data cells in table row.")

        data_cell_link_a_tag = table_row_link_data_cell.find("a")

        if data_cell_link_a_tag is None:
            raise RuntimeError("Could not find a tag in table data cell.")
        elif isinstance(data_cell_link_a_tag, NavigableString):
            raise RuntimeError("Cannot traverse instance of NavigatableString.")
        elif isinstance(data_cell_link_a_tag, int):
            raise RuntimeError("Cannot traverse instance of int.")

        title = data_cell_link_a_tag.get("title")

        if title is None:
            raise RuntimeError("Could not obtain href from table data cell.")
        elif isinstance(title, List):
            return title[0]

        return title

    def get_file_name(self) -> str:
        link = self.get_link()

        if link is not str or link.isspace():
            return "unknown.zip"

        decoded_filename = unquote(self.get_link())
        formatted_filename = sub(r"[^\w\s-]", "", decoded_filename).replace(" ", "_")

        return formatted_filename

    def get_link(self) -> str:
        table_row_link_data_cell = self.content.find("td", attrs={"class": "link"})

        if table_row_link_data_cell is None:
            raise RuntimeError("Could not find link tag in table row.")

        data_cell_link_a_tag = table_row_link_data_cell.find("a")

        if data_cell_link_a_tag is None:
            raise RuntimeError("Could not find a tag in table data cell.")
        elif isinstance(data_cell_link_a_tag, NavigableString):
            raise RuntimeError("Cannot traverse instance of NavigatableString.")
        elif isinstance(data_cell_link_a_tag, int):
            raise RuntimeError("Cannot traverse instance of int.")

        href = data_cell_link_a_tag.get("href")

        if href is None:
            raise RuntimeError("Could not obtain href from table data cell.")
        elif isinstance(href, List):
            return href[0]

        return href

    def get_size(self) -> str:
        return super().get_size()

    def get_date(self) -> str:
        return super().get_date()


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
            parsed_table_rows.append(MyrientGame(table_row))

        return parsed_table_rows

    def download(self, link: str, file_name: str) -> str:
        if self.save_path is None:
            raise RuntimeError("Property SAVE_PATH not provided.")

        file_url = urljoin(self.value, link)
        file_path = path.join(self.save_path, self.value, file_name)

        if path.isfile(file_path):
            print(f"File {file_name} already exists!")
            return file_path

        download_result = HttpContent(file_url).download(file_path)

        if download_result.is_failure():
            raise RuntimeError(f"Download failed due to: {download_result.content}")

        return download_result.content
