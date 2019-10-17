import re

from lucina.token import Token


def parse_file(filename):
    code = False

    with open(filename) as f:
        for line in f:
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
                yield Token.AFTER_TITLE(line, level=level)
            elif line.startswith('---'):
                yield Token.SPLIT(line)
            elif line.startswith('```'):
                code = True
                args = line[3:].split()
                skip = 'skip' in args
                yield Token.START_CODE(line, language=args[0], skip=skip)
            else:
                yield Token.LINE(line)


def parse_files(filenames):
    for filename in filenames:
        yield from parse_file(filename)
        yield Token.FILE()
