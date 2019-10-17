import enum


class _Token:
    def __init__(self, _type, line=None, **kwargs):
        self.type = _type
        self.line = line
        self.params = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        args = []
        if self.line is not None:
            args.append(repr(self.line))
        for key, value in self.params.items():
            args.append(f'{key}={value!r}')

        return f"{self.type}({', '.join(args)})"


class Token(enum.Enum):
    def __call__(self, *args, **kwargs):
        return _Token(self, *args, **kwargs)

    LINE = enum.auto()
    FILE = enum.auto()
    TITLE = enum.auto()
    AFTER_TITLE = enum.auto()
    SPLIT = enum.auto()
    START_CODE = enum.auto()
    END_CODE = enum.auto()
