from typing import List

from lucina.cell import Cell
from lucina.cell import CellType
from lucina.cell import SlideType
from lucina.tokenizer import Token


def clean_source(source: List[str]):
    lines = source[:]

    while lines and not lines[0].rstrip('\r\n'):
        lines.pop(0)
    while lines and not lines[-1].rstrip('\r\n'):
        lines.pop()

    if lines:
        lines[-1] = lines[-1].rstrip('\r\n')

    return lines


def split_cells(tokens, title_split, title_split_after):
    cell_type, lines = CellType.MARKDOWN, []
    for token in tokens:
        if token.type is Token.FILE:
            pass
        elif token.type is Token.TITLE:
            if token.level in title_split:
                yield cell_type, lines
                yield 'separator', title_split[token.level]
                cell_type, lines = CellType.MARKDOWN, [token.line]
            else:
                lines.append(token.line)
        elif token.type is Token.AFTER_TITLE:
            if token.level in title_split_after:
                yield cell_type, lines
                yield 'separator', title_page[token.level]
                cell_type, lines = CellType.MARKDOWN, []
        elif token.type is Token.SPLIT:
            yield cell_type, lines
            yield 'separator', SlideType.SUBSLIDE
            cell_type, lines = CellType.MARKDOWN, []
        elif token.type is Token.START_CODE:
            yield cell_type, lines
            yield 'separator', SlideType.SKIP if token.skip else SlideType.CONTINUE
            cell_type, lines = CellType.CODE, []
        elif token.type is Token.END_CODE:
            yield cell_type, lines
            cell_type, lines = CellType.MARKDOWN, []
        elif token.line is not None:
            lines.append(token.line)
    yield cell_type, lines


def parse_cells(tokens, title_split, title_split_after):
    slide_type = SlideType.CONTINUE
    for cell_type, content in split_cells(tokens, title_split, title_split_after):
        if cell_type == 'separator':
            if content != SlideType.CONTINUE: # Continuation
                slide_type = content
            continue
        source = clean_source(content)
        if source:
            yield Cell(cell_type, slide_type, source)
            slide_type = SlideType.CONTINUE
