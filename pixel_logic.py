from solve import solve_puzzle, Cell
from renderer import RENDERER, get_renderer


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


def main():
    row_constraints = load_input("Row constraints: ")
    col_constraints = load_input("Col constraints: ")

    cells = solve_puzzle(row_constraints, col_constraints)
    renderer = get_renderer(RENDERER.ASCII)

    renderer.render(cells, row_constraints, col_constraints)


if __name__ == "__main__":
    main()
