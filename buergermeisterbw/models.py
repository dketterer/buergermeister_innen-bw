from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum


class BuergermeisterArt(Enum):
    Buergermeister = 1
    Oberbuergermeister = 2


@dataclass_json
@dataclass
class Municipality:
    name: str
    link: str
    comment: str = ""
    zustimmung: float = .0
    wahlsieger: str = ""
    partei: str = ""
    wahlbeteiligung: float = .0
    einwohnerzahl: int = 0
    wahlberechtigte: int = 0
    buergermeister_art: BuergermeisterArt = 0
