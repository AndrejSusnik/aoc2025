file = 'input'
# file = 'example'

grid = list(map(str.strip, open(file).readlines()))
removed = 0
did_remove = True
while did_remove:
    accessible = 0
    new_grid = grid.copy()
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] != '@':
                continue
            rols = 0
            for k in range(-1, 2):
                for z in range(-1, 2):
                    if k == 0 and z == 0:
                        continue
                    if i - k < 0 or i - k > len(grid) - 1:
                        continue
                    if j - z < 0 or j - z > len(grid[0]) - 1:
                        continue

                    if grid[i-k][j-z] == '@':
                        rols += 1
            if rols < 4:
                accessible += 1        
                new_grid[i] = new_grid[i][:j] + '.' + new_grid[i][j+1:]
    removed += accessible
    did_remove = accessible > 0
    grid = new_grid

    

print(removed)
