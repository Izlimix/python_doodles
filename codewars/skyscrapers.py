"""
    Problem statement: https://www.codewars.com/kata/5671d975d81d6c1c87000022
    Solves a skyscraper puzzle of size 4x4, with clues given in clockwise order.

    Recursive brute-force solution based off of sudoku.py solver.
    Note: Can try a more elegant solution that just generates permutations of 1-4 for
      each row of grid, without storing state (no need to explicitly backtrack).
    Note: Can also try validating just the next possible move, rather than the whole grid every time it recurses.
"""

def solve_puzzle(clues):
    n = len(clues) // 4
    grid = [[None for _ in range(n)] for _ in range(n)]
    symbols = set(range(1, n+1))
    sol = _brute_recursive(clues, grid, symbols, side=n)
    if sol:
        return tuple(tuple(row) for row in sol)
    else:
        return None

def _brute_recursive(clues, grid, symbols, *, blanksym=None, side=None):
    if not _is_valid(clues, grid, symbols, blanksym=blanksym, side=side):
        return None

    pos = _next_blank(grid)
    if not pos:
        # No more blanks, solved.
        return grid
    else:
        (x, y) = pos
        possibles = symbols - _neighbours(grid, pos)
        for v in possibles:
            grid[x][y] = v
            attempt = _brute_recursive(clues, grid, symbols, blanksym=blanksym, side=side)
            if attempt:
                return attempt #Solved
            else:
                grid[x][y] = blanksym
        return None

def _is_valid(clues, grid, symbols, *, blanksym=None, side=None):
    # Does the incomplete grid violate any rules?
    # The height of the skyscrapers is between 1 and 4 (or is incomplete)
    heights = symbols.union({blanksym})
    if not all(e in heights for row in grid for e in row):
        return False

    # No two skyscrapers in a row or column may have the same number of floors (except blanksym)
    for row in grid:
        floors = [f for f in row if f is not blanksym]
        if len(set(floors)) < len(floors):
            return False
    for c in range(len(grid[0])):
        col = _col(grid, c)
        floors = [f for f in col if f is not blanksym]
        if len(set(floors)) < len(floors):
            return False

    # Clues
    (vert_clues, horiz_clues) = _pair_clues(clues, n=side)
    for i in range(len(vert_clues)):
        # column clues valid?
        (c1, c2) = vert_clues[i]
        col = _col(grid, i)
        if not _check_row(col, c1, c2):
            return False

    for i in range(len(horiz_clues)):
        #row clues valid?
        (c2, c1) = horiz_clues[i]
        row = grid[i]
        if not _check_row(row, c1, c2):
            return False

    return True

def _check_row(seq, c1, c2):
    vis_l = _count_visible(seq)
    vis_r = _count_visible(seq[::-1])
    if None not in seq:
        # If the row is complete, then the clues should be exact (if not 0).
        return ((not c1) or vis_l == c1) and ((not c2) or vis_r == c2)
    else:
        # Incomplete row, just check for "good enough"
        return ((not c1) or vis_l <= c1) and ((not c2) or vis_r <= c2)

def _neighbours(grid, pos, *, blanksym=None):
    (x, y) = pos
    ns = set(grid[x])
    ns.update(_col(grid, y))
    ns.remove(blanksym)
    return ns

def _next_blank(grid, *, blanksym=None):
    # Next blank (None) in l-r, top-bottom order
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[x][y] is blanksym:
                return (x, y)
    return None

def _count_visible(seq, *, blanksym=None):
    # Take values while next value is > the prev highest.
    # Stops if it reaches a blank (since whatever's placed there might block the count later)
    highest = 0
    count = 0
    for v in seq:
        if v is blanksym:
            break
        if v > highest:
            highest = v
            count += 1
    return count

def _col(grid, c):
    return [col[c] for col in grid]

def _pair_clues(clues, n=None):
    # Given a list of clues that correspond to cols/rows in clockwise order,
    # for some grid-size n (default: sqrt of len clues)
    if n is None:
        n = len(clues) // 4
    # Returns two lists ([cols], [rows]), where each element is a pair of clues for the same col/row
    cols = list(zip(clues[:n], clues[2*n:3*n][::-1]))
    rows = list(zip(clues[n:2*n], clues[3*n:][::-1]))
    return (cols, rows)
