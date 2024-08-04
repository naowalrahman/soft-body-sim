Web VPython 3.2

DT = 0.001
G = 70
MASS = 100
KS = 70000
KD = 500
MAX_X = 300
MAX_Y = 200
LENGTH = 50
MIN_LENGTH = 20


class Point:
    """
    Point mass that includes position, velocity, force, and a shape object
    to hold the sphere that represents the point mass visually.
    Use update_pos and update(self) to update the position of the point
    based on the forces acting on it.
    """
    def __init__(self, x, y, id):
        # z-component isn't use but is required by vpython
        self.pos = vector(x, y, 0)
        self.vel = vector(0, 0, 0)
        self.force = vector(0, 0, 0)
        self.shape = sphere(pos=self.pos, radius=10, color=color.red)
        self.id = id
    
    # euler integrate over time to get position
    def update(self):
        self.vel += self.force / MASS * DT
        self.pos += self.vel * DT
        self.shape.pos = self.pos
    
    # for debugging purposes
    def log(self):
        print(f"{self.id}:")
        print(f"\tforce:\t{self.force}")
        print(f"\tvelocity:\t{self.vel}")
        print(f"\tposition:\t{self.pos}")


class Spring:
    """
    Spring class that holds the two point masses that the spring connects, the
    rest length, and a curve object to visually represent the spring.
    """
    
    def __init__(self, beg, end):
        # attributes of the spring
        # beg and end are points
        self.beg = beg
        self.end = end
        self.length = mag(end.pos - beg.pos)
        # the shape of the spring depends on the beginning/ending point
        self.shape = curve(pos=[beg.pos, end.pos], color=color.yellow)
        
    # Once euler integration is done for each point mass, the spring's length
    # and position is updated with this 
    def update(self):
        self.shape.modify(0, pos=self.beg.pos)
        self.shape.modify(1, pos=self.end.pos)
  
  
# helper function tot clamp the position of the points within the frame
def signum(x):
    if x > 0:       return 1
    else if x < 0:  return -1
    else:           return 0


# represents the 8 cardinal directions and their intermediate values
dx = [1, 0, -1,  0, 1, -1,  1, -1]
dy = [0, 1,  0, -1, 1, -1, -1,  1]

# recursively dfs on a grid of point masses to connect them all with springs.
# uses an edge matrix rather than a boolean visited array since visits
# are pairwise in this scenario. 
def floodfill(has_edge, i, j, parent_i, parent_j):
    if parent_i != -1 and parent_j != -1:
        springs.append(Spring(masses[parent_i][parent_j], masses[i][j]))
        has_edge[masses[parent_i][parent_j].id][masses[i][j].id] = True
        has_edge[masses[i][j].id][masses[parent_i][parent_j].id] = True
        
    for k in range(len(dx)):
        new_i, new_j = i + dx[k], j + dy[k]
        if new_i < 0 or new_i >= body_height or new_j < 0 or new_j >= body_width:
            continue
        if not has_edge[masses[i][j].id][masses[new_i][new_j].id]:
            floodfill(has_edge, new_i, new_j, i, j)


# draw the soft body and call floodfill to connect with springs
def generate_body():
    global body_width, body_height, masses, springs
    
    masses = []
    springs = []
    start_x = -(LENGTH * (body_width - 1)) / 2
    start_y = -(LENGTH * (body_height - 1)) / 2
    
    for i in range(body_height):
        masses.append([])
        for j in range(body_width):
            masses[i].append(Point(start_x + j * LENGTH, start_y + i * LENGTH, i * body_width + j))
    
    area = body_width * body_height
    has_edge = [[False for _ in range(area)] for _ in range(area)]
    floodfill(has_edge, 0, 0, -1, -1)
            

# deletes the scene and generates a new one
def reset():
    global scene
    
    if scene is not None:
        scene.delete()
    
    scene = canvas(width=800, height=600, align="left")
    box(pos=vector(0, -MAX_Y - 17, 0), size=vector(634, 10, 1))
    box(pos=vector(0, MAX_Y + 17, 0), size=vector(634, 10, 1))
    box(pos=vector(-MAX_X - 17, 0, 0), size=vector(10, 434, 1))
    box(pos=vector(MAX_X + 17, 0, 0), size=vector(10, 434, 1))
    

# deletes the graph curve and starts a new curve
# regenerates the soft-body body
def regen():
    global yyDots
    yyDots.delete()
    reset()
    generate_body()
    

# change global constants based on updated user input (if the user moves the slider)
def change_const(event):
    global body_width, body_height, G, KD, KS, MASS, LENGTH
    id, val = event.id, event.value
    if id == "body width":
        body_width = val
    elif id == "body height":
        body_height = val
    elif id == "gravity":
        G = val
    elif id == "damping constant":
        KD = val
    elif id == "spring constant":
        KS = val
    elif id == "mass":
        MASS = val
    elif id == "spring length":
        LENGTH = val  


scene = None
body_width, body_height = 1, 2
masses, springs = None, None

reset()
   
# generates the graph, some captions, the reset button, and the sliders
g1 = graph(width=350, height=250, xtitle="time (s)", ytitle="Net Kinetic Energy (J)", align="right")
yyDots = gcurve(color=color.green, graph=g1)
scene.caption = " Body width"
width_slider = slider(bind=change_const, min=1, max=8, step=1, value=body_width, id="body width", align="left")
scene.append_to_caption("\n Body height")
height_slider = slider(bind=change_const, min=1, max=6, step=1, value=body_height, id="body height", align="left")
scene.append_to_caption("\n Spring constant")
ks_slider = slider(bind=change_const, min=70000, max=150000, step=100, value=KS, id="spring constant", align="left")
scene.append_to_caption("\n Damping constant")
kd_slider = slider(bind=change_const, min=100, max=1500, step=50, value=KD, id="damping constant", align="left")
scene.append_to_caption("\n Mass")
mass_slider = slider(bind=change_const, min=50, max=150, step=10, value=MASS, id="mass", align="left")
scene.append_to_caption("\n Spring length")
length_slider = slider(bind=change_const, min=30, max=50, step=1, value=LENGTH, id="spring length", align="left")
scene.append_to_caption("\n\n")
reset_button = button(bind=regen, text='reset', background=color.cyan, align="left")

scene.append_to_caption("\n\nUse the arrow keys to move around the soft body!\n\n")

# using a boolean to track whether the user is applying an external velocity on the soft body
user_movement = False

# let the user move the body with arrow keys
def key_input(evt):
    global max_compressed, user_movement
    keys = keysdown()
    user_movement = any(["left" in keys, "right" in keys, "down" in keys, "up" in keys])
    
    # don't apply a velocity if too compressed to prevent breaking
    v = 0 if max_compressed else 150
    for mass_list in masses:
        # setting the else to 0 so that the soft body stops moving on key up
        # (needed because we don't have air resistance)
        for mass in mass_list:
            if "left" in keys:
                mass.vel.x = -v
            elif "right" in keys:
                mass.vel.x = v
            else:
                mass.vel.x = 0
            if "down" in keys:
                mass.vel.y = -v
            elif "up" in keys:
                mass.vel.y = v
            else:
                mass.vel.y = 0

# binds the arrow keys to the function key_input
scene.bind('keydown keyup', key_input)
    
regen()

t = 0
max_compressed = False
while True:
    rate(1 / DT)
        
    for mass_list in masses:
        for mass in mass_list:
            mass.force = vector(0, -MASS * G, 0)
            
    max_compressed = False
    
    for spring in springs:
        p1, p2 = spring.beg, spring.end
            
        # spring & dampening force
        u = norm(p2.pos - p1.pos)
        dist = mag(p1.pos - p2.pos)
        fs = KS * (dist - spring.length)
        fd = u.dot(p2.vel - p1.vel) * KD
        ft = fs + fd
        p1.force += u * ft
        p2.force -= u * ft
        
        if dist < MIN_LENGTH:
            max_compressed = True
            
        spring.update()
        
    yy = 0
    

    for mass_list in masses:
        for mass in mass_list:
            # clamp the position if it is above the limit 
            if abs(mass.pos.y) >= MAX_Y:
                mass.pos.y = MAX_Y * signum(mass.pos.y)
            if abs(mass.pos.x) >= MAX_X:
                mass.pos.x = MAX_X * signum(mass.pos.x)
            if not user_movement:
                if abs(mass.pos.y) >= MAX_Y:
                    mass.vel.y = -mass.vel.y
                if abs(mass.pos.x) >= MAX_X:
                    mass.vel.x = -mass.vel.x
            
            # accumulate the total kinetic energy
            yy += 0.5 * MASS * mag(mass.vel) ** 2
            mass.update()
            
    # update time and graph
    t += DT
    yyDots.plot(t, yy)
