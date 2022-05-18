from prettytable import MSWORD_FRIENDLY, PrettyTable
from solve import row, solve_puzzle

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

def draw_table(cells, row_constraints, col_constraints):
    ROWS = len(row_constraints)
    COLS = len(col_constraints)
    x = PrettyTable(header=False)
    def fmt(x): return "X" if x == 1 else ""
    x.set_style(MSWORD_FRIENDLY)
    x.add_row([""] + [col_constraints[c] for c in range(COLS)])
    for row in range(ROWS):
        data = [row_constraints[row]] + \
            [fmt(cells[(row, col)].value) for col in range(COLS)]
        x.add_row(data)

    print(x)

def main():
    row_constraints = load_input("Row constraints: ")    
    col_constraints = load_input("Col constraints: ") 
    ROWS = len(row_constraints)
    COLS = len(col_constraints)

    cells = solve_puzzle(row_constraints, col_constraints)

    draw_table(cells, row_constraints, col_constraints)   

if __name__ == "__main__":
    main()