#!/usr/bin/python3

from modules.core import ConsoleFactory, ConsoleType


def main():
    """
    entry point for script
    """
    game_title = input("Please input your game title: ")
    game_console = input("Please input the console: ")

    game_console = ConsoleType.from_string(game_console)
    console = ConsoleFactory(game_console).create_console()


if __name__ == "__main__":
    main()
