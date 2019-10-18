from lucina.tokenizer import Token
from lucina.tokenizer import tokenize_file
from lucina.tokenizer import tokenize_files


def test_token():
    token = Token.SPLIT()
    assert token.type is Token.SPLIT
    assert token.line is None
    assert token.params == {}
    assert repr(token) == "Token.SPLIT()"

    token = Token.LINE('foobar')
    assert token.type is Token.LINE
    assert token.line == 'foobar'
    assert token.params == {}
    assert repr(token) == "Token.LINE('foobar')"

    token = Token.TITLE('# foobar', level=1)
    assert token.type is Token.TITLE
    assert token.line == '# foobar'
    assert token.level == 1
    assert token.params == {'level': 1}
    assert repr(token) == "Token.TITLE('# foobar', level=1)"


def test_tokenize_file_simple():
    content = [
        'abc\n',
        'def\n',
        '\n',
    ]
    assert list(tokenize_file(content)) == [
        Token.LINE('abc\n'),
        Token.LINE('def\n'),
        Token.LINE('\n'),
    ]


def test_tokenize_file_title():
    content = [
        '# Document\n',
        '## First\n',
        '* ok\n',
        '* well\n',
        '## Then\n',
        'content\n',
    ]
    assert list(tokenize_file(content)) == [
        Token.TITLE('# Document\n', level=1),
        Token.AFTER_TITLE(level=1),
        Token.TITLE('## First\n', level=2),
        Token.AFTER_TITLE(level=2),
        Token.LINE('* ok\n'),
        Token.LINE('* well\n'),
        Token.TITLE('## Then\n', level=2),
        Token.AFTER_TITLE(level=2),
        Token.LINE('content\n'),
    ]


def test_tokenize_file_split():
    content = [
        'abc\n',
        '----------\n',
        'def\n',
    ]
    assert list(tokenize_file(content)) == [
        Token.LINE('abc\n'),
        Token.SPLIT('----------\n'),
        Token.LINE('def\n'),
    ]


def test_tokenize_file_code():
    content = [
        'abc\n',
        '\n',
        '```python\n',
        'def random():\n',
        '    return 4\n',
        '```\n',
        '\n',
        '```python skip',
        'print(random())\n',
        '```\n',
    ]

    assert list(tokenize_file(content)) == [
        Token.LINE('abc\n'),
        Token.LINE('\n'),
        Token.START_CODE('```python\n', language='python', skip=False),
        Token.LINE('def random():\n'),
        Token.LINE('    return 4\n'),
        Token.END_CODE('```\n'),
        Token.LINE('\n'),
        Token.START_CODE('```python skip', language='python', skip=True),
        Token.LINE('print(random())\n'),
        Token.END_CODE('```\n'),
    ]


def test_tokenize_files():
    contents = [
        ['# First file\n', 'Hey\n'],
        ['# Second file\n', 'Ho\n'],
    ]

    assert list(tokenize_files(contents)) == [
        Token.FILE(),
        Token.TITLE('# First file\n', level=1),
        Token.AFTER_TITLE(level=1),
        Token.LINE('Hey\n'),
        Token.AFTER_FILE(),
        Token.FILE(),
        Token.TITLE('# Second file\n', level=1),
        Token.AFTER_TITLE(level=1),
        Token.LINE('Ho\n'),
        Token.AFTER_FILE(),
    ]
