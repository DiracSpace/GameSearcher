from enum import IntEnum
from pydantic import BaseModel


class ConsoleTypeEnum(IntEnum):
    unknown = 1
    playstation_1 = 2
    playstation_2 = 3
    playstation_3 = 4
    playstation_4 = 5
    playstation_5 = 6
    gamecube = 7
