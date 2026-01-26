import random
import turtle


board = []
for r in range(0,9):
    for c in range(0,9):
        board += [(r, c)]


player_pos = random.choice(board)
target_pos = random.choice(board)


occupied = set()
occupied.add(player_pos)
occupied.add(target_pos)

walls = []
wall_positions = set()
num_walls = 6


for _ in range(num_walls):
    attempts = 0
    while attempts < 100:  
        orientation = random.choice(['horizontal', 'vertical'])
        
        if orientation == 'horizontal':
            r = random.randint(0, 8)
            c = random.randint(0, 7)
            wall = [(r, c), (r, c+1)]
        else:
            r = random.randint(0, 7)
            c = random.randint(0, 8)
            wall = [(r, c), (r+1, c)]
        
        if all(pos not in occupied for pos in wall):
            walls.append(wall)
            occupied.update(wall)
            break
        
        attempts += 1

wall_positions = set()
for wall in walls:
    wall_positions.update(wall)

#Manhatten Distance  h = abs (current_cell.x – goal.x) + abs (current_cell.y – goal.y)
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
distance = manhattan_distance(player_pos, target_pos)


g_values = {player_pos: 0} #How many steps to get here 

open_set = [player_pos] #Places I need to check
closed_set = set() #Places fully explored
came_from = {} # What Direction did I come from

#print("-" * 50)
#print(board)
print("-" * 50)
print("Player Position:", player_pos)
print("Target Position:", target_pos)
print("Walls:", walls)
print("Manhattan Distance:", distance)
print("-" * 50)

while open_set:
    """

1 ) Pick optimal location from open_set
2 ) Look at each neighbor, for min item in open_set
3 ) Record how to get to each neighbor and how far it is
4 ) Add neighbors to "to-check" list
5 ) Put current pos in closed_set because its explored
    
    """
    current = min(open_set, key=lambda pos: g_values.get(pos, float('inf')) + manhattan_distance(pos, target_pos)) # find lowest f = g + h

    if current == target_pos:
        constructed_path = []
        current = target_pos
        while current in came_from:
            constructed_path.append(current)
            current = came_from[current]
        constructed_path.append(player_pos)
        constructed_path.reverse()
        print("Path found:", constructed_path)
        break
    elif current != target_pos and not open_set:
        print("No Path Found")
        break
    else:
        

        open_set.remove(current)
        closed_set.add(current)

        r,c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)] # Direction for neighbors

        for neighbor in neighbors:
            nr, nc = neighbor
            if 0 <= nr <= 8 and 0 <= nc <= 8 and neighbor not in wall_positions and neighbor not in closed_set: # Valid
                tentative_g = g_values[current] + 1

                if neighbor not in g_values or tentative_g < g_values[neighbor]:
                    g_values[neighbor] = tentative_g # Records how far tenative neighbor is from start
                    came_from[neighbor] = current # Records how to get there
                    if neighbor not in open_set:
                        open_set.append(neighbor)
    
print("-" * 50)



screen = turtle.Screen()
screen.bgcolor("white") 
screen.setup(width=1000, height=1000)
t = turtle.Turtle() 
t.color("black") 
screen.tracer(0)




def draw_nodes(player_position, target_position, wall_positions, color):
    for node in board:
        x, y = node
        screen_x = (x - 4) * 50  
        screen_y = (y - 4) * 50  
        t.penup()
        t.goto(screen_x, screen_y)
        
        if node == player_position:
            t.dot(20, "green")  
        elif node == target_position:
            t.dot(20, "red")    
        elif node in wall_positions:
            t.dot(20, "blue")  
        else:
            t.dot(10, color)


draw_nodes(player_pos, target_pos, wall_positions, "black")
screen.update()


def draw_path(path, color):
    for node in path:
        x, y = node
        screen_x = (x - 4) * 50  
        screen_y = (y - 4) * 50  
        t.penup()
        t.goto(screen_x, screen_y)
        t.dot(15, color)

draw_path(constructed_path, "yellow")
screen.mainloop() 