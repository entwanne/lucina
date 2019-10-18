from lucina.cell import Cell
from lucina.cell import CellType
from lucina.cell import SlideType


def test_cell():
    cell1 = Cell()
    assert cell1.cell_type is CellType.MARKDOWN
    assert cell1.slide_type is SlideType.CONTINUE
    assert cell1.source == []

    cell2 = Cell(CellType.CODE, SlideType.SLIDE, ['foo', 'bar'])
    assert cell2.cell_type is CellType.CODE
    assert cell2.slide_type is SlideType.SLIDE
    assert cell2.source == ['foo', 'bar']

    cell3 = Cell('code', 'slide', ['foo', 'bar'])
    assert cell3.cell_type is CellType.CODE
    assert cell3.slide_type is SlideType.SLIDE
    assert cell3.source == ['foo', 'bar']

    assert cell1 != cell2
    assert cell2 == cell3
