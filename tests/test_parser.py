from lucina.cell import Cell
from lucina.cell import SlideType
from lucina.parser import SplitRules
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


def test_split_rules():
    rules = SplitRules({
        SlideType.SLIDE: [Token.TITLE(level=1)],
        SlideType.FRAGMENT: [Token.TITLE(), Token.SPLIT()],
        SlideType.SUBSLIDE:  [Token.TITLE(level=2)],
    })

    match = rules.match(Token.TITLE('# foo', level=1))
    assert match == (True, SlideType.SLIDE)

    match = rules.match(Token.TITLE('## foo', level=2))
    assert match == (True, SlideType.SUBSLIDE)

    match = rules.match(Token.TITLE('### foo', level=3))
    assert match == (True, SlideType.FRAGMENT)

    match = rules.match(Token.SPLIT())
    assert match == (True, SlideType.FRAGMENT)

    match = rules.match(Token.FILE())
    assert match == (False, None)


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


def test_parse_cells_no_splits():
    cells = list(parse_cells(TOKENS, {}))
    assert cells == [
        Cell('markdown', 'slide', [
            '# 111\n',
            '\n',
            '* bullet point\n',
            '* bullet point 2\n',
            '\n',
            '```python\n',
            'def random():\n',
            '    return 4\n',
            '```\n',
            '\n',
            '---\n',
            '\n',
            '```python\n',
            'print(random())\n',
            '```\n',
            '\n',
            '---\n',
            '\n',
            'Text.\n',
            '## 222\n',
            '\n',
            '```python skip\n',
            'import itertools\n',
            '```\n',
            '\n',
            'Hello world.',
        ]),
    ]


def test_parse_cells_code_split():
    split_rules = {
        SlideType.CONTINUE: [Token.START_CODE(), Token.END_CODE()],
        SlideType.SKIP: [Token.START_CODE(skip=True)],
    }
    cells = list(parse_cells(TOKENS, split_rules))
    assert cells == [
        Cell('markdown', 'slide', [
            '# 111\n', '\n', '* bullet point\n', '* bullet point 2',
        ]),
        Cell('code', '-', ['def random():\n', '    return 4']),
        Cell('markdown', '-', ['---']),
        Cell('code', '-', ['print(random())']),
        Cell('markdown', '-', ['---\n', '\n', 'Text.\n', '## 222']),
        Cell('code', 'skip', ['import itertools']),
        Cell('markdown', '-', ['Hello world.']),
    ]


def test_parse_cells_horizontal_split():
    split_rules = {SlideType.SUBSLIDE: [Token.SPLIT()]}
    cells = list(parse_cells(TOKENS, split_rules))
    assert cells == [
        Cell('markdown', 'slide', [
            '# 111\n',
            '\n',
            '* bullet point\n',
            '* bullet point 2\n',
            '\n',
            '```python\n',
            'def random():\n',
            '    return 4\n',
            '```',
        ]),
        Cell('markdown', 'subslide', [
            '```python\n',
            'print(random())\n',
            '```',
        ]),
        Cell('markdown', 'subslide', [
            'Text.\n',
            '## 222\n',
            '\n',
            '```python skip\n',
            'import itertools\n',
            '```\n',
            '\n',
            'Hello world.',
        ]),
    ]


def test_parse_cells_title_splits():
    split_rules = {
        SlideType.SLIDE: [Token.TITLE(level=1)],
        SlideType.SUBSLIDE: [Token.TITLE(level=2)],
    }
    cells = list(parse_cells(TOKENS, split_rules))
    assert cells == [
        Cell('markdown', 'slide', [
            '# 111\n',
            '\n',
            '* bullet point\n',
            '* bullet point 2\n',
            '\n',
            '```python\n',
            'def random():\n',
            '    return 4\n',
            '```\n',
            '\n',
            '---\n',
            '\n',
            '```python\n',
            'print(random())\n',
            '```\n',
            '\n',
            '---\n',
            '\n',
            'Text.',
        ]),
        Cell('markdown', 'subslide', [
            '## 222\n',
            '\n',
            '```python skip\n',
            'import itertools\n',
            '```\n',
            '\n',
            'Hello world.',
        ]),
    ]

    split_rules = {
        SlideType.SLIDE: [Token.TITLE(level=1)],
        SlideType.SUBSLIDE: [Token.AFTER_TITLE(level=1), Token.TITLE(level=2)],
    }
    cells = list(parse_cells(TOKENS, split_rules))
    assert cells == [
        Cell('markdown', 'slide', ['# 111']),
        Cell('markdown', 'subslide', [
            '* bullet point\n',
            '* bullet point 2\n',
            '\n',
            '```python\n',
            'def random():\n',
            '    return 4\n',
            '```\n',
            '\n',
            '---\n',
            '\n',
            '```python\n',
            'print(random())\n',
            '```\n',
            '\n',
            '---\n',
            '\n',
            'Text.',
        ]),
        Cell('markdown', 'subslide', [
            '## 222\n',
            '\n',
            '```python skip\n',
            'import itertools\n',
            '```\n',
            '\n',
            'Hello world.',
        ]),
    ]


def test_parse_cells_combine_split():
    split_rules = {
        SlideType.SLIDE: [Token.TITLE(level=1)],
        SlideType.SUBSLIDE: [Token.AFTER_TITLE(level=1), Token.TITLE(level=2)],
        SlideType.FRAGMENT: [Token.SPLIT()],
        SlideType.CONTINUE: [Token.START_CODE(), Token.END_CODE()],
        SlideType.SKIP: [Token.START_CODE(skip=True)],
    }
    cells = list(parse_cells(TOKENS, split_rules))
    assert cells == [
        Cell('markdown', 'slide', ['# 111']),
        Cell('markdown', 'subslide', ['* bullet point\n', '* bullet point 2']),
        Cell('code', '-', ['def random():\n', '    return 4']),
        Cell('code', 'fragment', ['print(random())']),
        Cell('markdown', 'fragment', ['Text.']),
        Cell('markdown', 'subslide', ['## 222']),
        Cell('code', 'skip', ['import itertools']),
        Cell('markdown', '-', ['Hello world.']),
    ]
