"""
Pixel logic solver

+-----+-------+----------+----------+
|     |  1,1  |    2     |    1     |
+=====+=======+==========+==========+
| 2   |   X   |    X     |          |
| 1   |       |    X     |          |
| 1,1 |   X   |          |    X     |
+-----+-------+----------+----------+

Row constraints specify the total number of Xs in each row layed out contiguously (i.e. no gaps).
Col constraints specify the total number of Xs in each column layed out contiguously (i.e. no gaps).

If there are two numbers then there should be two contiguous segements separated by at least one space.

Example constraints
row_constraints = [
    [5],
    [7],
    [3, 2],
    [3, 3],
    [2, 6],
    [2, 5, 1],
    [2, 1, 1, 1],
    [2, 1, 1, 1],
    [1, 1],
    [7]
]

col_constraints = [
    [5],
    [7],
    [3, 1],
    [3, 4, 1],
    [2, 2, 1],
    [2, 4, 1],
    [2, 3, 1],
    [8, 1],
    [4, 1],
    [1, 1]
]

"""
from typing import List, Tuple

import pyomo.environ as pyo
from prettytable import MSWORD_FRIENDLY, PrettyTable
from pyomo.core.expr.numeric_expr import ExpressionBase
from pyomo.environ import (ConcreteModel, Constraint, ConstraintList, Model,
                           SolverFactory)
from pyomo.gdp import Disjunction

Cell = Tuple[int, int]


def load_input(prompt):
    print(prompt)
    constraints = []
    i = 0
    while True:
        res = input(f"{i + 1}. :")
        if res.strip().lower() == "x":
            break
        if int(res) == 10:
            constraints.append([10])
        else:
            constraints.append([int(c) for c in res])
        i += 1
    return constraints


def draw_table(model, row_constraints, col_constraints, ROWS, COLS):
    x = PrettyTable(header=False)
    def fmt(x): return "X" if x == 1 else ""
    x.set_style(MSWORD_FRIENDLY)
    x.add_row([""] + [col_constraints[c] for c in range(COLS)])
    for row in range(ROWS):
        data = [row_constraints[row]] + \
            [fmt(model.cells[(row, col)].value) for col in range(COLS)]
        x.add_row(data)

    print(x)


def _generate_disjunction(model: Model, cells: List[Cell], constraints: List[int]) -> List[ExpressionBase]:
    """
    Recursively step through constraint segments and generate all the possible solution
    Returns an array of expressions
    """
    if len(constraints) == 0:
        return []

    spaces = len(constraints) - 1
    cells_needed = sum(constraints) + spaces

    disjuncts = []
    while len(cells) >= cells_needed:
        constraint = constraints[0]
        cell_run = cells[0:constraint]
        padding = 1
        sub_disjuncts = _generate_disjunction(
            model, cells[constraint + padding:], constraints[1:])
        d = sum(model.cells[c]
                for c in cell_run) == constraint   # type: ignore

        if len(constraints[1:]) > 0:
            for sub_d in sub_disjuncts:
                disjuncts.append([d] + sub_d)  # type: ignore
        else:
            disjuncts.append([d])

        cells = cells[1:]

    return disjuncts


def generate_disjunction(model: Model, cells: List[Cell], constraints: List[int]) -> List[ExpressionBase]:
    """ Generate disjunction of expressions """
    disjunctions = _generate_disjunction(model, cells, constraints)

    return disjunctions


def generate_constraint(model, cells, constraint) -> ExpressionBase:
    return (sum(model.cells[cell] for cell in cells) == sum(constraint))


def row(idx, COLS) -> List[Cell]:
    return [(idx, col) for col in range(COLS)]


def col(idx, ROWS) -> List[Cell]:
    return [(row, idx) for row in range(ROWS)]


def main():
    row_constraints = load_input("Row constraints: ")    
    col_constraints = load_input("Col constraints: ")    

    ROWS = len(row_constraints)
    COLS = len(col_constraints)

    index_list = [
        (i, j)
        for i in range(len(row_constraints))
        for j in range(len(col_constraints))
    ]

    model = ConcreteModel()
    model.cells = pyo.Var(index_list, domain=pyo.Binary)
    model.N = pyo.Set(initialize=range(ROWS))
    model.M = pyo.Set(initialize=range(COLS))
    model.row_constraints = row_constraints
    model.col_constraints = col_constraints

    constraints = ConstraintList()
    constraints.construct()

    for idx, row_constraint in enumerate(row_constraints):
        c = generate_constraint(model, row(idx, COLS), row_constraints[idx])
        constraints.add(c)

    for idx, col_constraint in enumerate(col_constraints):
        c = generate_constraint(model, col(idx, ROWS), col_constraints[idx])
        constraints.add(c)

    model.c = constraints

    model.r0 = Disjunction(expr=generate_disjunction(
        model, row(0, COLS), row_constraints[0]))
    model.r1 = Disjunction(expr=generate_disjunction(
        model, row(1, COLS), row_constraints[1]))
    model.r2 = Disjunction(expr=generate_disjunction(
        model, row(2, COLS), row_constraints[2]))
    model.r3 = Disjunction(expr=generate_disjunction(
        model, row(3, COLS), row_constraints[3]))
    model.r4 = Disjunction(expr=generate_disjunction(
        model, row(4, COLS), row_constraints[4]))
    model.r5 = Disjunction(expr=generate_disjunction(
        model, row(5, COLS), row_constraints[5]))
    model.r6 = Disjunction(expr=generate_disjunction(
        model, row(6, COLS), row_constraints[6]))
    model.r7 = Disjunction(expr=generate_disjunction(
        model, row(7, COLS), row_constraints[7]))
    model.r8 = Disjunction(expr=generate_disjunction(
        model, row(8, COLS), row_constraints[8]))
    if len(row_constraints) == 10:
        model.r9 = Disjunction(expr=generate_disjunction(
            model, row(9, COLS), row_constraints[9]))

    model.c0 = Disjunction(expr=generate_disjunction(
        model, col(0, ROWS), col_constraints[0]))
    model.c1 = Disjunction(expr=generate_disjunction(
        model, col(1, ROWS), col_constraints[1]))
    model.c2 = Disjunction(expr=generate_disjunction(
        model, col(2, ROWS), col_constraints[2]))
    model.c3 = Disjunction(expr=generate_disjunction(
        model, col(3, ROWS), col_constraints[3]))
    model.c4 = Disjunction(expr=generate_disjunction(
        model, col(4, ROWS), col_constraints[4]))
    model.c5 = Disjunction(expr=generate_disjunction(
        model, col(5, ROWS), col_constraints[5]))
    model.c6 = Disjunction(expr=generate_disjunction(
        model, col(6, ROWS), col_constraints[6]))
    model.c7 = Disjunction(expr=generate_disjunction(
        model, col(7, ROWS), col_constraints[7]))
    model.c8 = Disjunction(expr=generate_disjunction(
        model, col(8, ROWS), col_constraints[8]))
    if len(col_constraints) == 10:
        model.c9 = Disjunction(expr=generate_disjunction(
            model, col(9, ROWS), col_constraints[9]))

    obj = sum(model.cells[i, j] for i in range(ROWS) for j in range(COLS))
    model.OBJ = pyo.Objective(expr=obj, sense=pyo.maximize)

    results = SolverFactory("gdpopt").solve(
        model, strategy="LOA", mip_solver="cbc")

    draw_table(model, row_constraints, col_constraints, ROWS, COLS)


if __name__ == "__main__":
    main()
