from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple

from minimd.tokenizer import Token

from lucina.cell import Cell
from lucina.cell import CellType
from lucina.cell import SlideType


_KEEP_CONTENT_ON_SPLIT = {Token.TITLE}
_SPLIT_CELL_TYPE = {Token.START_CODE: CellType.CODE}


class SplitRules:
    def __init__(self, split_rules: Dict[SlideType, List[Token]]):
        self.rules = {}
        for slide_type, token_patterns in split_rules.items():
            for token_pattern in token_patterns:
                rules = self.rules.setdefault(token_pattern.type, [])
                rules.append((token_pattern.params, slide_type))

        for rules in self.rules.values():
            rules[:] = sorted(rules, key=lambda r: len(r[0]), reverse=True)

    def match(self, token: Token) -> Tuple[bool, SlideType]:
        for rule, slide_type in self.rules.get(token.type, ()):
            if all(token.params.get(k) == v for k, v in rule.items()):
                return True, slide_type
        return False, None


def clean_source(source: List[str]) -> List[str]:
    lines = source[:]

    while lines and not lines[0].rstrip('\r\n'):
        lines.pop(0)
    while lines and not lines[-1].rstrip('\r\n'):
        lines.pop()

    if lines:
        lines[-1] = lines[-1].rstrip('\r\n')

    return lines


def _split_cells(tokens, split_rules):
    split_rules = SplitRules(split_rules)
    cell_type, lines = CellType.MARKDOWN, []
    for token in tokens:
        split, slide_type = split_rules.match(token)

        if split:
            yield cell_type, lines
            yield None, slide_type
            cell_type = _SPLIT_CELL_TYPE.get(token.type, CellType.MARKDOWN)
            lines = []
            if token.type not in _KEEP_CONTENT_ON_SPLIT:
                continue

        if token.content is not None:
            lines.append(token.content)

    yield cell_type, lines


def parse_cells(
        tokens: Iterable[Token],
        split_rules: Dict[SlideType, List[Token]],
) -> Iterable[Cell]:
    slide_type = SlideType.SLIDE
    for cell_type, content in _split_cells(tokens, split_rules):
        if cell_type is None:
            if slide_type is None or content.rank < slide_type.rank:
                slide_type = content
            continue

        source = clean_source(content)
        if source:
            yield Cell(cell_type, slide_type or SlideType.CONTINUE, source)
            slide_type = None
