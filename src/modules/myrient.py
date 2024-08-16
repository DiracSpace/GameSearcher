#!/usr/bin/python3

from enum import Enum
from dataclasses import dataclass
from typing import List


class MyrientConsole(Enum):
    unknown = "unknown"
    playstation_3 = "playstation_3"
    gamecube = "gamecube"

    @staticmethod
    def from_string(console: str):
        console = console.lower().strip()
        if console in "unknown":
            return MyrientConsole.unknown
        elif console in "playstation_3" or console in "playstation 3":
            return MyrientConsole.playstation_3
        elif console in "gamecube":
            return MyrientConsole.gamecube
        else:
            raise NotImplementedError(f"Unsupported console {console}.")

    @staticmethod
    def domains(console: str) -> List[str]:
        return [
            domain.value
            for domain in MYRENT_DOMAINS
            if domain.key == MyrientConsole.from_string(console)
        ]


@dataclass
class MyrientDomain:
    key: MyrientConsole
    value: str


MYRENT_DOMAINS: List[MyrientDomain] = [
    MyrientDomain(
        MyrientConsole.playstation_3,
        "https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%203%20(PSN)%20(Content)/",
    ),
    MyrientDomain(
        MyrientConsole.playstation_3,
        "https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%203%20(PSN)%20(Updates)/",
    ),
    MyrientDomain(
        MyrientConsole.gamecube,
        "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20[zstd-19-128k]/",
    ),
]
