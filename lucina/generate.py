from lucina.cell import clean_cell
from lucina.cell import make_cell
from lucina.parser import parse_files
from lucina.token import Token


def get_cells(filenames, title_split, title_split_after):
    cell_type, lines = 'markdown', []
    for token in parse_files(filenames):
        if token.type is Token.FILE:
            pass
        elif token.type is Token.TITLE:
            if token.level in title_split:
                yield cell_type, lines
                yield 'separator', title_split[token.level]
                cell_type, lines = 'markdown', [token.line]
            else:
                lines.append(token.line)
        elif token.type is Token.AFTER_TITLE:
            if token.level in title_split_after:
                yield cell_type, lines
                yield 'separator', title_page[token.level]
                cell_type, lines = 'markdown', []
        elif token.type is Token.SPLIT:
            yield cell_type, lines
            yield 'separator', 'subslide'
            cell_type, lines = 'markdown', []
        elif token.type is Token.START_CODE:
            yield cell_type, lines
            yield 'separator', 'skip' if token.skip else '-'
            cell_type, lines = 'code', []
        elif token.type is Token.END_CODE:
            yield cell_type, lines
            cell_type, lines = 'markdown', []
        elif token.line is not None:
            lines.append(token.line)
    yield cell_type, lines


def generate_cells(filenames, title_split, title_split_after):
    cells = []
    slide_type = '-'
    for cell_type, content in get_cells(filenames, title_split, title_split_after):
        if cell_type == 'separator':
            if content != '-': # Continuation
                slide_type = content
            continue
        cell = make_cell(cell_type, content, slide_type)
        cell = clean_cell(cell)
        if cell['source']:
            cells.append(cell)
            slide_type = '-'
    return cells
