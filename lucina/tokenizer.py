import enum
import re
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import TextIO


class Token(enum.Enum):
    def __call__(self, *args, **kwargs):
        return _Token(self, *args, **kwargs)

    LINE = enum.auto()
    FILE = enum.auto()
    AFTER_FILE = enum.auto()
    TITLE = enum.auto()
    AFTER_TITLE = enum.auto()
    SPLIT = enum.auto()
    START_CODE = enum.auto()
    END_CODE = enum.auto()


@dataclass
class _Token:
    type: Token
    content: str
    params: Dict[str, Any]

    def __init__(self, _type: Token, content: str = None, **kwargs):
        self.type = _type
        self.content = content
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.params = kwargs
        if content is not None:
            self.params['content'] = content

    def __repr__(self) -> str:
        args = []
        if self.content is not None:
            args.append(repr(self.content))
        for key, value in self.params.items():
            if key != 'content':
                args.append(f'{key}={value!r}')

        return f"{self.type}({', '.join(args)})"


def tokenize_file(file: TextIO) -> Iterable[Token]:
    code = False

    for line in file:
        if code:
            if line.startswith('```'):
                code = False
                yield Token.END_CODE(line)
            else:
                yield Token.LINE(line)
            continue

        match = re.match(r'(#+) ', line)
        if match:
            level = len(match.group(1))
            yield Token.TITLE(line, level=level)
            yield Token.AFTER_TITLE(level=level)
        elif line.startswith('---'):
            yield Token.SPLIT(line)
        elif line.startswith('```'):
            code = True
            args = line[3:].split()
            skip = 'skip' in args
            yield Token.START_CODE(line, language=args[0], skip=skip)
        else:
            yield Token.LINE(line)


def tokenize_files(files: List[TextIO]) -> Iterable[Token]:
    for file in files:
        yield Token.FILE()
        yield from tokenize_file(file)
        yield Token.AFTER_FILE()
