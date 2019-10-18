from lucina.cell import Cell
from lucina.format import format_cell
from lucina.format import format_cells
from lucina.format import format_doc


def test_format_cell():
    cell = Cell('markdown', 'fragment', ['foo  \n', '  bar\n'])
    assert format_cell(cell) == {
        'cell_type': 'markdown',
        'metadata': {
            'scrolled': True,
            'slideshow': {
                'slide_type': 'fragment',
            },
        },
        'source': ['foo  \n', '  bar\n'],
    }

    cell = Cell('markdown', 'subslide', [])
    assert format_cell(cell) == {
        'cell_type': 'markdown',
        'metadata': {
            'scrolled': True,
            'slideshow': {
                'slide_type': 'subslide',
            },
        },
        'source': [],
    }

    cell = Cell('code', 'subslide', ['def random():\n', '    return 4\n'])
    assert format_cell(cell) == {
        'cell_type': 'code',
        'metadata': {
            'scrolled': True,
            'slideshow': {
                'slide_type': 'subslide',
            },
        },
        'source': ['def random():\n', '    return 4\n'],
        'outputs': [],
        'execution_count': None,
    }


def test_format_cells():
    c1 = Cell('markdown', 'fragment', ['foo  \n', '  bar\n'])
    c2 = Cell('code', 'subslide', ['def random():\n', '    return 4\n'])

    assert list(format_cells([c1, c2])) == [format_cell(c1), format_cell(c2)]


def test_format_doc():
    cells = [
        Cell('markdown', 'fragment', ['foo  \n', '  bar\n']),
        Cell('code', 'subslide', ['def random():\n', '    return 4\n']),
    ]

    doc = format_doc(cells)
    assert doc['cells'] == list(format_cells(cells))
    assert (doc['nbformat'], doc['nbformat_minor']) == (4, 2)
    assert doc['metadata']['celltoolbar'] == 'Slideshow'
    assert doc['metadata']['language_info']['name'] == 'python'
    assert doc['metadata']['livereveal']['autolaunch'] is True

    doc = format_doc(cells, autolaunch=False)
    assert doc['metadata']['livereveal']['autolaunch'] is False
