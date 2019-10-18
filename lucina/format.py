from lucina.cell import Cell
from lucina.cell import CellType


def format_cell(cell: Cell):
    doc = {
        'cell_type': cell.cell_type.value,
        'metadata': {
            'scrolled': True,
            'slideshow': {
                'slide_type': cell.slide_type.value,
            },
        },
        'source': cell.source,
    }

    if cell.cell_type == CellType.CODE:
        doc['outputs'] = []
        doc['execution_count'] = None

    return doc


def format_cells(cells):
    for cell in cells:
        yield format_cell(cell)


def format_doc(cells, autolaunch=True):
    return {
        'cells': list(format_cells(cells)),
        'metadata': {
            'celltoolbar': 'Slideshow',
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            },
            'language_info': {
                'codemirror_mode': {
                    'name': 'ipython',
                    'version': 3
                },
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.6.5'
            },
            "livereveal": {
                "autolaunch": autolaunch,
            }
        },
        'nbformat': 4,
        'nbformat_minor': 2,
    }
