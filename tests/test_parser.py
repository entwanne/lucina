from lucina.cell import Cell
from lucina.parser import clean_source
from lucina.parser import parse_cells
from lucina.tokenizer import Token


TOKENS = [
    Token.FILE(),
    Token.TITLE('# 111\n', level=1),
    Token.AFTER_TITLE(level=1),
    Token.LINE('\n'),
    Token.LINE('* bullet point\n'),
    Token.LINE('* bullet point 2\n'),
    Token.LINE('\n'),
    Token.START_CODE('```python\n', language='python', skip=False),
    Token.LINE('def random():\n'),
    Token.LINE('    return 4\n'),
    Token.END_CODE('```\n'),
    Token.LINE('\n'),
    Token.SPLIT('---\n'),
    Token.LINE('\n'),
    Token.START_CODE('```python\n', language='python', skip=False),
    Token.LINE('print(random())\n'),
    Token.END_CODE('```\n'),
    Token.LINE('\n'),
    Token.SPLIT('---\n'),
    Token.LINE('\n'),
    Token.LINE('Text.\n'),
    Token.AFTER_FILE(),
    Token.FILE(),
    Token.AFTER_FILE(),
    Token.FILE(),
    Token.TITLE('## 222\n', level=2),
    Token.AFTER_TITLE(level=2),
    Token.LINE('\n'),
    Token.START_CODE('```python skip\n', language='python', skip=True),
    Token.LINE('import itertools\n'),
    Token.END_CODE('```\n'),
    Token.LINE('\n'),
    Token.LINE('Hello world.\n'),
    Token.AFTER_FILE(),
]


def test_clean_source():
    source = [
        '\n',
        '\r\n',
        'foo\n',
        '\n',
        'bar\n',
        '\n',
    ]
    ret = clean_source(source)
    assert ret != source  # no in-place change
    assert ret == ['foo\n', '\n', 'bar']

    source = [
        'foo\n',
        'bar\n',
    ]
    assert clean_source(source) == ['foo\n', 'bar']

    source = ['\n']
    assert clean_source(source) == []


def test_parse_cells_no_title_splits():
    cells = list(parse_cells(TOKENS, {}, {}))
    assert cells == [
        Cell('markdown', '-', [
            '# 111\n', '\n', '* bullet point\n', '* bullet point 2',
        ]),
        Cell('code', '-', ['def random():\n', '    return 4']),
        Cell('code', 'subslide', ['print(random())']),
        Cell('markdown', 'subslide', ['Text.\n', '## 222']),
        Cell('code', 'skip', ['import itertools']),
        Cell('markdown', '-', ['Hello world.']),
    ]


def test_parse_cells_title_splits():
    cells = list(parse_cells(TOKENS, {1: 'slide'}, {}))
    assert cells == [
        Cell('markdown', 'slide', [
            '# 111\n', '\n', '* bullet point\n', '* bullet point 2',
        ]),
        Cell('code', '-', ['def random():\n', '    return 4']),
        Cell('code', 'subslide', ['print(random())']),
        Cell('markdown', 'subslide', ['Text.\n', '## 222']),
        Cell('code', 'skip', ['import itertools']),
        Cell('markdown', '-', ['Hello world.']),
    ]

    cells = list(parse_cells(TOKENS, {1: 'slide', 2: 'subslide'},
                             {1: 'slide'}))
    assert cells == [
        Cell('markdown', 'slide', ['# 111']),
        Cell('markdown', 'slide', ['* bullet point\n', '* bullet point 2']),
        Cell('code', '-', ['def random():\n', '    return 4']),
        Cell('code', 'subslide', ['print(random())']),
        Cell('markdown', 'subslide', ['Text.']),
        Cell('markdown', 'subslide', ['## 222']),
        Cell('code', 'skip', ['import itertools']),
        Cell('markdown', '-', ['Hello world.']),
    ]
