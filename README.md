# pixel-logic-solver
Non-linear optimisation to solve the Pixel Logic game

The Pixel Logic game is an n x m grid with row and column constraints.
```
+-----+-------+----------+----------+
|     |  1,1  |    2     |    1     |
+=====+=======+==========+==========+
| 2   |   X   |    X     |          |
| 1   |       |    X     |          |
| 1,1 |   X   |          |    X     |
+-----+-------+----------+----------+

```

Row constraints specify the total number of Xs in each row layed out contiguously (i.e. no gaps).
Col constraints specify the total number of Xs in each column layed out contiguously (i.e. no gaps).

If there are two numbers then there should be two contiguous segements separated by at least one space.
e.g. 1, 1 cannot be `[X|X| | ]` it needs to be `[X| |X| ]` or `[X| | |X]`

Example constraints
```
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
```

```
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
```

I'm not ashamed to say that I built this because I couldn't beat my kid's highscore without cheating. Amazingly even with this solver, I am only a few seconds faster than his best time.


solve.py still needs to be improved, especially the creation of the disjunctions which are currently hardcoded to 9 or 10 columns and rows.

# Installation
- sudo apt install coinor-cbc
- python -m venv .env
- source .env/bin/activate
- python -m pip install -r requirements.txt

This script is currently user the cbc solver, it is possible to change this by updating the get_solver() function in solve.py

# Run
- python solve.py

