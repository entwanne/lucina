import enum
from dataclasses import dataclass
from dataclasses import field
from typing import List


class CellType(enum.Enum):
    MARKDOWN = 'markdown'
    CODE = 'code'


class SlideType(enum.Enum):
    CONTINUE = '-'
    SLIDE = 'slide'
    SUBSLIDE = 'subslide'
    FRAGMENT = 'fragment'
    SKIP = 'skip'
    NOTES = 'notes'


@dataclass
class Cell:
    cell_type: CellType = CellType.MARKDOWN
    slide_type: SlideType = SlideType.CONTINUE
    source: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.cell_type = CellType(self.cell_type)
        self.slide_type = SlideType(self.slide_type)
