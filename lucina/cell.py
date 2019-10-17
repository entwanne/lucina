import enum
from dataclasses import dataclass


def make_cell(cell_type, source, slide_type='-'):
    cell = {
        'cell_type': cell_type,
        'metadata': {
            'scrolled': True,
            'slideshow': {
                'slide_type': slide_type,
            },
        },
        'source': source,
    }

    if cell_type == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

    return cell


def clean_cell(cell):
    lines = cell['source']

    while lines and not lines[0].rstrip('\r\n'):
        lines.pop(0)
    while lines and not lines[-1].rstrip('\r\n'):
        lines.pop()

    if lines:
        lines[-1] = lines[-1].rstrip('\r\n')

    return cell


class CellType(enum.IntEnum):
    MARKDOWN = enum.auto()
    CODE = enum.auto()


class SlideType(enum.IntEnum):
    CONTINUE = enum.auto()
    SLIDE = enum.auto()
    SUBSLIDE = enum.auto()
    FRAGMENT = enum.auto()
    SKIP = enum.auto()
    NOTES = enum.auto()


@dataclass
class Cell:
    cell_type: CellType
    slide_type: SlideType
    source: list
