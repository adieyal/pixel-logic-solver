from typing import Iterator, List, Protocol

from prettytable import MSWORD_FRIENDLY, PrettyTable
from solve import Cell
from enum import Enum


class RENDERER(Enum):
    ASCII = "ascii"


class Renderer(Protocol):
    def render(
        self,
        cells: Iterator[Cell],
        row_constraints: List[int],
        col_constraints: List[int],
    ):
        ...


class AsciiRender:
    def render(
        self,
        cells: Iterator[Cell],
        row_constraints: List[int],
        col_constraints: List[int],
    ):
        self._draw_table(cells, row_constraints, col_constraints)

    def _draw_table(
        self,
        cells: Iterator[Cell],
        row_constraints: List[int],
        col_constraints: List[int],
    ):
        ROWS = len(row_constraints)
        COLS = len(col_constraints)
        x = PrettyTable(header=False)

        def fmt(x):
            return "X" if x == 1 else ""

        x.set_style(MSWORD_FRIENDLY)
        x.add_row([""] + [col_constraints[c] for c in range(COLS)])
        for row in range(ROWS):
            data = [row_constraints[row]] + [
                fmt(cells[(row, col)].value) for col in range(COLS)
            ]
            x.add_row(data)

        print(x)


def get_renderer(key: RENDERER) -> Renderer:
    if key == RENDERER.ASCII:
        return AsciiRender()
    raise ValueError(f"Unknown renderer: {key}")
