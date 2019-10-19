import enum
from dataclasses import dataclass
from dataclasses import field
from typing import List

from lucina.utils import ordered_enum


class CellType(enum.Enum):
    MARKDOWN = 'markdown'
    CODE = 'code'


@ordered_enum
class SlideType(enum.Enum):
    SLIDE = 'slide'
    SUBSLIDE = 'subslide'
    FRAGMENT = 'fragment'
    CONTINUE = '-'
    NOTES = 'notes'
    SKIP = 'skip'


@dataclass
class Cell:
    cell_type: CellType = CellType.MARKDOWN
    slide_type: SlideType = SlideType.CONTINUE
    source: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.cell_type = CellType(self.cell_type)
        self.slide_type = SlideType(self.slide_type)
