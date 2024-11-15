Cols = "ABCDEFGHI"
Rows = set(range(1, 10))

def reset_board(grid):
    for row in Rows:
        for col in Cols:
            grid[f"{col}{row}"] = Rows.copy()

grid = {}
reset_board(grid)

def load_puzzle(grid, filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for row, line in enumerate(lines, 1):
            line = line.strip()
            for col, char in enumerate(line, 1):
                if char != '0':
                    grid[f"{Cols[col-1]}{row}"] = {int(char)}

load_puzzle(grid, 'board.txt')

def generate_rows():
    rows_list = []
    for row in Rows:
        row_cells = []
        for col in Cols:
            row_cells.append(f"{col}{row}")
        rows_list.append(row_cells)
    return rows_list

def generate_columns():
    cols_list = []
    for col in Cols:
        col_cells = []
        for row in Rows:
            col_cells.append(f"{col}{row}")
        cols_list.append(col_cells)
    return cols_list

def generate_blocks():
    col_groups = [Cols[0:3], Cols[3:6], Cols[6:9]]
    row_groups = [list(range(1, 4)), list(range(4, 7)), list(range(7, 10))]
    blocks = []
    for row_group in row_groups:
        for col_group in col_groups:
            block_cells = []
            for row in row_group:
                for col in col_group:
                    block_cells.append(f"{col}{row}")
            blocks.append(block_cells)
    return blocks

def apply_all_diff_constraint(grid, cell_group):
    modified = False
    for cell1 in cell_group:
        if len(grid[cell1]) == 1:
            for cell2 in cell_group:
                if cell1 != cell2:
                    previous_values = grid[cell2].copy()
                    grid[cell2].discard(list(grid[cell1])[0])
                    if previous_values != grid[cell2]:
                        modified = True
    return modified

def apply_equals_constraint_v2(grid, group):
    modified = False
    matching_pairs = {}
    for cell1 in group:
        if len(grid[cell1]) > 1:
            for cell2 in group:
                if cell1 != cell2 and grid[cell1] == grid[cell2]:
                    key = tuple(grid[cell1])
                    if key in matching_pairs:
                        cells_set = set(matching_pairs[key])
                        cells_set.update([cell1, cell2])
                        matching_pairs[key] = list(cells_set)
                    else:
                        matching_pairs[key] = [cell1, cell2]
    for domain, cells in matching_pairs.items():
        if len(domain) == len(cells):
            for cell in group:
                if cell not in cells:
                    for value in domain:
                        previous = grid[cell].copy()
                        grid[cell].discard(value)
                        if previous != grid[cell]:
                            modified = True
    return modified

def apply_equals_constraint(grid, group):
    modified = False
    for cell1 in group:
        if len(grid[cell1]) == 2:
            for cell2 in group:
                if cell1 != cell2 and grid[cell1] == grid[cell2]:
                    for cell3 in group:
                        if cell1 != cell3 and cell2 != cell3:
                            previous = grid[cell3].copy()
                            grid[cell3].discard(list(grid[cell1])[0])
                            grid[cell3].discard(list(grid[cell1])[1])
                            if previous != grid[cell3]:
                                modified = True
    return modified

def solve_puzzle(grid, constraints):
    if is_completed(grid):
        return True

    cell = pick_unassigned_cell(grid)
    possible_values = grid[cell].copy()

    for value in possible_values:
        if is_allowed(grid, cell, value):
            grid[cell] = {value}

            if solve_puzzle(grid, constraints):
                return True

            grid[cell] = possible_values

    return False

def is_completed(grid):
    return all(len(grid[cell]) == 1 for cell in grid)

def pick_unassigned_cell(grid):
    for cell in grid:
        if len(grid[cell]) > 1:
            return cell

def is_allowed(grid, cell, value):
    for group in constraints:
        if cell in group:
            for other_cell in group:
                if other_cell != cell and len(grid[other_cell]) == 1 and list(grid[other_cell])[0] == value:
                    return False
    return True

constraints = generate_rows() + generate_columns() + generate_blocks()

solve_puzzle(grid, constraints)

for row in Rows:
    for col in Cols:
        print(list(grid[f"{col}{row}"])[0], end=" ")
    print()
