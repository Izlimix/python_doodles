#!/usr/bin/env python3


# A basic sudoku solver.

# Sudokus in the form of 9x9 2D arrays, where arr[0] gives the first row.

import collections

def is_solved(grid):
    # Is the given grid a solved (and valid) sudoku puzzle?
    """
    out = True
    numbers = set(range(1,10))
    # Is the grid 9x9?
    out = out and len(grid) == 9 and all(len(row) == 9 for row in grid)
    # Does every row use up 1-9?
    out = out and all(set(row) == numbers for row in grid)
    # Does every column use up 1-9?
    out = out and all(set(column(grid, i)) == numbers for i in range(len(grid[0])))
    # Does every 3x3 square use up 1-9?
    out = out and all(set(chunk) == numbers for chunk in chunks(grid))
    return out
    """
    return valid_shape(grid) \
            and all(valid_numbers(row) for row in grid) \
            and all(valid_numbers(column(grid, i)) for i in range(9)) \
            and all(valid_numbers(chunk) for chunk in chunks(grid))

def valid_shape(grid, size=9):
    return len(grid) == size and all(len(row) == size for row in grid)

def valid_numbers(section, size=9):
    return set(section) == set(range(1, size + 1))

def valid_move(grid, pos, value):
    (x, y) = pos
    """
    # Does the row already contain that value?
    if value in grid[x]: return False
    # Does the column already contain that value?
    if value in column(grid, y): return False
    # Does the chunk already contain that value?
    if value in chunk(grid, pos): return False
    
    return True
    """
    return value not in grid[x] and value not in column(grid, y) and value not in chunk_of(grid, pos)

def column(grid, col):
    return (grid[row][col] for row in range(len(grid)))

def chunks(grid, chunk_size=3):
    size = len(grid)
    for offset_x in range(0, size, chunk_size):
        for offset_y in range(0, size, chunk_size):
            #yield (grid[offset_x + x][offset_y + y] for x in range(chunk_size) for y in range(chunk_size))
            yield chunk_from(grid, offset_x, offset_y, chunk_size)
            
def chunk_of(grid, pos, chunk_size=3):
    # Return the chunk which pos lies in
    (x, y) = pos
    offset_x = x - (x % chunk_size)
    offset_y = y - (y % chunk_size)
    return chunk_from(grid, offset_x, offset_y, chunk_size)

def chunk_from(grid, offset_x, offset_y, chunk_size=3):
    # Returns an nxn chunk from any given offset
    return (grid[offset_x + x][offset_y + y] for x in range(chunk_size) for y in range(chunk_size))

def visible_from(grid, pos, chunk_size=3):
    (x, y) = pos
    visible = set(grid[x]) #Row
    visible.update(column(grid, y)) #Column
    visible.update(chunk_of(grid, pos, chunk_size)) #Chunk
    return visible
    
def snakeify(grid):
    return [e for row in grid for e in row]

def unsnakeify(row, row_length=9):
    return [row[offset : offset + row_length] for offset in range(0, len(row), row_length)]

# Note: this doesn't work properly with the solver by default, since the returned grid is full of strings rather than ints.
def line_to_grid(line, sep=None, blank_symbol=None, grid_size=9, symbols=None):
    if symbols is None:
        symbols = set(str(i) for i in range(1, grid_size+1))
    out = []
    vals = line.split(sep)
    for offset in range(0, len(vals), grid_size):
        row = []
        for i in range(0, grid_size):
            v = vals[offset+i]
            if v not in symbols:
                v = blank_symbol
            row.append(v)
        out.append(row)
    return out

def cleanup_vals(grid):
    numbers = set(range(1, 10))
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] not in numbers:
                grid[x][y] = None
                
def unique_numbers(section):
    numbers = set(range(1, 10))
    section = [n for n in section if n in numbers]
    return len(section) == len(set(section))
                
def no_contradictions(grid):
    # Every row, column and chunk should not contain more than 1 copy of any number in {1-9}
    return all(unique_numbers(row) for row in grid) \
            and all(unique_numbers(column(grid, c)) for c in range(len(grid[0]))) \
            and all(unique_numbers(chunk) for chunk in chunks(grid))
                
def blanks(grid):
    return ((x, y) for x in range(len(grid)) for y in range(len(grid[x])) if not grid[x][y])

def next_blank(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if not grid[x][y]: return (x, y)
    return None
    
def brute_recursive(grid, *, default_blank=None, symbols={1,2,3,4,5,6,7,8,9}):
    pos = next_blank(grid)
    if not pos:
        # No more blanks, solved.
        return grid
    else:
        (x, y) = pos
        possibles = symbols - visible_from(grid, pos)
        for v in possibles:
            grid[x][y] = v
            attempt = brute_recursive(grid)
            if attempt:
                return attempt #Solved
            else:
                grid[x][y] = default_blank
        return None
    
# Brute-force:
def brute_force(grid):
    #todo
    # Find the first blank spot (False-y?). If there aren't any, it's solved! (Unless the initial grid had contradictions)
    # Attempt to place values from 1-9 in that spot
    #   if invalid move, go back and try the next number.
    #   otherwise continue brute-forcing the rest of the grid.
    # All the numbers for this cell are invalid/lead to contradictions? Backtrack and pick a different number for the previous cell
    assert valid_shape(grid)
    cleanup_vals(grid)
    assert no_contradictions(grid)
    
    moves = collections.deque() # Backtrack-able moves previously made
    
    bl = next_blank(grid)
    while bl:
        (x, y) = bl
        #.......
        
    
    return