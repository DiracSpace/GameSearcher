from typing import List
from core.core import ConsoleType
from core.myrient import MyrientSource


MYRENT_DOMAINS: List[MyrientSource] = [
    MyrientSource(
        ConsoleType.PLAYSTATION_1,
        "https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%203%20(PSN)%20(Content)/",
    ),
    MyrientSource(
        ConsoleType.PLAYSTATION_1,
        "https://myrient.erista.me/files/No-Intro/Sony%20-%20PlayStation%203%20(PSN)%20(Updates)/",
    ),
    MyrientSource(
        ConsoleType.GAMECUBE,
        "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20[zstd-19-128k]/",
    ),
]
