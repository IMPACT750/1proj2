def verify_barriers(walls, start_cell, end_cell):
# Check if there is a path from the start cell to the end cell.
  #queue = [(start_cell, heuristic(start_cell, end_cell))]
  queue = [(start_cell,None)]

  visited = set()
  print("__________________________________________________________")
  while queue:
    cell,parent = queue.pop(0)
    #cell = get_min(queue)
    visited.add(cell)
    print(cell)

    # Check if the current cell is the end cell.
    if cell == end_cell:
      return True

    # Check if there is a path from the current cell to the end cell.
    for neighbor in get_neighbors(cell, walls):
      if neighbor not in visited:
        queue.append((neighbor, cell))

  return False
def get_min(queue):
    mincell,minvalue = queue[0]
    for cell,value in queue:
        if value < minvalue:
            minvalue= value
    return mincell
def heuristic(start_cell, end_cell):
    y1 = start_cell[1]
    y2 = end_cell[1]
    return abs(y1 - y2)
def get_neighbors(cell, walls):
    neighbors = []
    x,y = cell
    if walls[x][y]["TOP"] == 0:
        neighbors.append((x, y - 1))
    if walls[x][y]["BOTTOM"] == 0:
        neighbors.append((x, y + 1))
    if walls[x][y]["LEFT"] == 0:
        neighbors.append((x - 1, y))
    if walls[x][y]["RIGHT"] == 0:
        neighbors.append((x + 1, y))

    return neighbors


