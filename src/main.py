#!/usr/bin/python3


from modules.core import ContentResponse, HttpContent
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import List
from dataclasses import dataclass
from urllib.parse import urljoin, unquote
from os import path, getenv
from re import sub
from dotenv import load_dotenv

load_dotenv()


SAVE_PATH = getenv("SAVE_PATH") or ""


class MyrientTableRow:
    table_row: Tag

    def __init__(self, table_row: Tag):
        self.table_row = table_row

    @property
    def link(self) -> str:
        table_row_link_data_cell = self.table_row.find("td", attrs={"class": "link"})

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

    @property
    def title(self) -> str:
        table_row_link_data_cell = self.table_row.find("td")

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

    @property
    def file_name(self) -> str:
        decoded_filename = unquote(self.link)
        formatted_filename = sub(r"[^\w\s-]", "", decoded_filename).replace(" ", "_")
        return formatted_filename

    def size(self) -> str:
        return ""

    def date(self) -> str:
        return ""


class MyrientPlaystation3Parser:
    content: BeautifulSoup
    query: str

    def __init__(self, content: str, query: str):
        self.content = BeautifulSoup(content, features="html.parser")
        self.query = query

    def parse_content(self) -> List[MyrientTableRow]:
        table = self.content.find("table", attrs={"id": "list"})

        if table is None:
            raise RuntimeError("Could not find table in provided content.")
        elif isinstance(table, NavigableString):
            raise RuntimeError("Cannot traverse instance of NavigatableString.")

        parsed_table_rows: List[MyrientTableRow] = []
        for index, table_row in enumerate(table.find_all("tr")):
            # skip headers and file traversal row
            if index == 0 or index == 1:
                continue
            elif table_row is None:
                continue
            parsed_table_rows.append(MyrientTableRow(table_row))
        return parsed_table_rows


@dataclass
class ConsoleParser:
    console: MyrientConsole
    content: ContentResponse
    domain: str
    query: str

    @property
    def results(self) -> List[MyrientTableRow]:
        print(f"Parsing console {self.console}.")
        parsed_results = []
        if self.console == MyrientConsole.playstation_3:
            parsed_results = MyrientPlaystation3Parser(
                self.content.content, self.query
            ).parse_content()
        elif self.console == MyrientConsole.gamecube:
            parsed_results = MyrientGamecubeParser(
                self.content.content, self.query
            ).parse_content()
        else:
            print(f"No parser found for {self.console}.")
            raise RuntimeError(f"Unsupported console: {self.console}")
        return [
            result
            for result in parsed_results
            if self.query.lower().strip() in result.title.lower().strip()
        ]


def prepare_download(game_domain: str, game_console: str, link: str, file_name: str):
    file_url = urljoin(game_domain, link)
    file_path = path.join(
        SAVE_PATH, MyrientConsole.from_string(game_console).value, file_name
    )

    if path.isfile(file_path):
        print(f"File {file_name} already exists!")
        return

    HttpContent(file_url).download(file_path)


def prepare_results_from_domain(
    domain: str, game_title: str, game_console: MyrientConsole
) -> List[MyrientTableRow]:
    http_content_response = HttpContent(domain).fetch_url_content()

    if http_content_response.is_failure():
        raise RuntimeError(
            f"Failure to obtain response content. Status Code: {http_content_response.status_code}, Message: {http_content_response.content}"
        )

    return ConsoleParser(
        game_console, http_content_response, domain, game_title
    ).results


def main():
    """
    entry point for script
    """
    game_title = input("Please input your game title: ")
    game_console = input("Please input the console: ")
    game_domains = MyrientConsole.domains(game_console)

    parsed_myrient_results: List[MyrientTableRow] = []
    for domain in game_domains:
        parsed_myrient_results = prepare_results_from_domain(
            domain, game_title, MyrientConsole.from_string(game_console)
        )

    if len(parsed_myrient_results) == 0:
        print(f"No results found for {game_title}.")
        exit(1)
    elif len(parsed_myrient_results) > 1:
        print("Please select a title by entering the corresponding number")
        for index, myrient_result in enumerate(parsed_myrient_results, start=1):
            print(f"{index} - {myrient_result.title}")
    else:
        prepare_download(
            parsed_myrient_results[0].link,
            MyrientConsole.from_string(game_console).value,
            parsed_myrient_results[0].link,
            parsed_myrient_results[0].title,
        )
        exit(0)

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(parsed_myrient_results):
                selected_result = parsed_myrient_results[choice - 1]
                print(f"You selected: {selected_result.title}")
                prepare_download(
                    selected_result.link,
                    MyrientConsole.from_string(game_console).value,
                    selected_result.link,
                    selected_result.file_name,
                )
        except ValueError:
            print("Please enter a valid choice.")


if __name__ == "__main__":
    main()
