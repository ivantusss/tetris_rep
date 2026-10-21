# import necessary things# import necessary things

from pygame import *
from sys import *
from random import *

# pygame initiation

init()

# special figure set

image_jesus = image.load('jesus.png')
image_jesus = transform.scale(image_jesus, (150, 200))

# drawing net (screen fill and net drawing function)

def net_draw():
    global a, b, screen

    #screen.fill((200, 200, 160))         # you can just fill screen in color you want
    
    for x in range(0, a +1, 50):
        draw.line(screen, (0, 0, 0), (x, 0), (x, b), 3)

    for y in range(0, b +1, 50):
        draw.line(screen, (0, 0, 0), (0, y), (a, y), 3)

# setting snd update any own back ground

def back_ground_draw(current_image):
    global a, b, screen

    back_ground = image.load(current_image).convert() # you can load your own background
    back_ground = transform.scale(back_ground, (a, b))

    screen.blit(back_ground, (0, 0))

# cube class for making figures

class Cube(sprite.Sprite):
    def __init__(self, x, y):

        # image attribute

        self.image = image.load('pivnoi_cube.png') # you can load your own cube photo
        self.image = transform.scale(self.image, (50, 50))
        
        # rect attributes

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# figure class

class Figure:

    # different figure forms

    forms = [
        [(0, 0), (0, -50), (0, -100), (0, -150)],    # stick
        [(0, 0), (0, -50), (50, -50), (100, -50)],   # left curvature
        [(0, 0), (0, -50), (-50, -50), (50, -50)],   # cross
        [(0, 0), (0, -50), (-50, -50), (-100, -50)], # right curvature
        [(0, 0), (50, 0), (0, -50), (-50, -50)],     # left zig zag
        [(0, 0), (50, 0), (50, -50), (100, -50)],    # right zig zag
        [(0, 0), (50, 0), (0, -50), (50, -50)],      # cube
        [(0, 0), (0, -50), (0, -100), (0, -150), (-50, -100), (50, -100)] # Jesus Christ
    ]

    # basic function for figure's cubes-attribute and random forms

    def __init__(self, x=None, y=None, first=False):
        # image attribure for special figure drawing

        self.image_rotate_degree = 0

        # cubes and central cube attributes

        if x is None or y is None: # requirement to avoid game crash
            self.cubes = []
            self.center_cube = None

        else:
            self.cubes = [
                Cube(x + increment_x, y + increment_y)
                for increment_x, increment_y in choice(
                    self.forms[:-1] if first else self.forms
                )                                              # mini function for custom position
            ]
            
            # central cube of rotation

            self.center_cube = self.cubes[1]

    # moving function

    def move(self, direction_x, direction_y):
        for cube in self.cubes:
            cube.rect.x += direction_x
            cube.rect.y += direction_y

    # moving requirement function
        
    def can_move(self, direction_x, direction_y):
        global a, b, court
        
        # if figure bumps into walls or floor

        for cube in self.cubes:
            if cube.rect.left + direction_x < 0:
                return False
            if cube.rect.right + direction_x > a:
                return False
            if cube.rect.bottom + direction_y > b:
                return False
            
            # if figure bumps into lying figures

            next_position = cube.rect.move(direction_x, direction_y)

            for cube in court.cubes:
                if next_position.colliderect(cube):
                    return False
        
        return True
    
    # rotate function

    def rotate(self):
        # coordinates of rotation center cube

        center_x = self.center_cube.rect.x
        center_y = self.center_cube.rect.y

        if not self.can_rotate():
            return
        
        for cube in self.cubes:

            # changing cube coordinates

            dx = cube.rect.x - center_x
            dy = cube.rect.y - center_y

            cube.rect.x = center_x - dy
            cube.rect.y = center_y + dx
        
        # rotate jesus image

        if len(self.cubes) == 6:
            self.image_rotate_degree = (self.image_rotate_degree - 90) % 360

    # rotate requirement function

    def can_rotate(self):
        global a, b, court

        # coordinates of rotation center cube

        center_x = self.center_cube.rect.x 
        center_y = self.center_cube.rect.y

        for cube in self.cubes:
        
            # rotated cube get_coordinates_formula

            dx = cube.rect.x - center_x
            dy = cube.rect.y - center_y

            new_x = center_x - dy
            new_y = center_y + dx
           
            # creating new cube

            rotated_rect = Rect(new_x, new_y, 50, 50)
        
            # if cube bumps into walls or floor 

            if rotated_rect.left < 0:
                return False
            if rotated_rect.right > a:
                return False
            if rotated_rect.bottom > b:
                return False
        
            # if cube bumps into lying figures

            for cube in court.cubes:
                if rotated_rect.colliderect(cube.rect):
                    return False
            
        return True
        
    # spawning new figure requirement function

    def spawn(self):
        global spawning, current_figure, forms
        
        if spawning == True:
            spawning = False

            current_figure = Figure(200, 0, first=False) # custom position

    # drawnig current figure function

    def draw(self, screen):
        # protection if center is None

        if not self.cubes:
            return

        # drawing special jesus figure

        if len(self.cubes) == 6:

            # getting drawing coordinates

            rotated_image = transform.rotate(
                image_jesus, self.image_rotate_degree
            )
            image_rect = rotated_image.get_rect(
                center=self.center_cube.rect.center
            )
            screen.blit(rotated_image, image_rect)

        # drawing regular cube image

        else: 
            for cube in self.cubes:
                screen.blit(cube.image, cube.rect)

# MAIN event checking cycle        

def event_checking():
    global running, court, spawning

    for ev in event.get():
        
        # leaving event

        if ev.type == QUIT:
            running = False
        
        # listening to keyboard and moving figure events 

        if ev.type == KEYDOWN:

            if ev.key == K_DOWN:
                if current_figure.can_move(0, 50):
                    current_figure.move(0, 50)
            
            if ev.key == K_LEFT:
                if current_figure.can_move(-50, 0):
                    current_figure.move(-50, 0)
            
            if ev.key == K_RIGHT:
                if current_figure.can_move(50, 0):
                    current_figure.move(50, 0)
            
            if ev.key == K_SPACE:
                current_figure.rotate()
        
        # figure fall event

        if ev.type == fall_event:
            if current_figure.can_move(0, 50):
                current_figure.move(0, 50)
            
            else:
                court.cubes += current_figure.cubes
                spawning = True

# distructing cubes-filled line in cubes_court 

def line_distruction_animation(): 
    global line_clear_waiting

    for y in range(0, b, 50):
        line = [
            cube for cube in court.cubes
            if cube.rect.y == y
        ]

        if len(line) == a//50 and y not in lines_to_clear:
            lines_to_clear.append(y)
            
            for cube in line:
                cube.image = transform.scale(
                    image.load('wave_of_distruction.png'),
                    (50, 50)
                )
        
    if lines_to_clear and line_clear_waiting is None:
        line_clear_waiting = time.get_ticks()

def line_distruction():
    global lines_to_clear, line_clear_waiting

    if line_clear_waiting is None:
        return

    if time.get_ticks() - line_clear_waiting < 500:
        return

    cleared_lines = lines_to_clear.copy()

    court.cubes = [
        cube for cube in court.cubes
        if cube.rect.y not in lines_to_clear
    ]

    for cube in court.cubes:
        lines_below = sum(
            1 for y in cleared_lines
            if cube.rect.y < y
        )
        
        cube.rect.y += lines_below * 50
    
    lines_to_clear = []
    line_clear_waiting = None
                
# MAIN game cycle function

def game_end():
    for cube in court.cubes:
        if cube.rect.y <= 0:
            return True

def game_running():
    global running

    while running: 

        event_checking()
        back_ground_draw('pivnoi_background.png')
        #net_draw()                       # you can make net on the screen
        line_distruction_animation()
        line_distruction()  
        current_figure.draw(screen)
        court.draw(screen)
        current_figure.spawn()

        display.update()

        if game_end():
            back_ground_draw('loose_background.png')
            display.update()
            time.wait(5000)
            return

# MAIN program

a, b = 500, 700                           # x, y axes. /50 to get ceils num 
screen = display.set_mode((a, b))
running = True

current_figure = Figure(200, 0, first=True)
spawning = False

fall_event = USEREVENT + 1                # making periodic event for figure falling
time.set_timer(fall_event, 800)           # MAIN time speed/time set

court = Figure([])                        # making laying cubes space                            

lines_to_clear = []
line_clear_waiting = None

game_running()                            # running a game function

quit()
exit()