import curses 
import math
from random import randint
from math import isclose

# step up ship and score
ship = (0,0)
score = 0

#Function defenition

# set the game canvas and difficulty level
def get_initial_input():
    while True:
        try:
            width = int(input("Please set canvas width (25 - 80): "))
            height = int(input("Please set canvas height (10 - 40): "))
            difficulty = int(input("Please select a difficulty level (1 - 5): "))
        except ValueError:
            print("Please input integer number")
            continue
        if width < 25 or width > 80 or height < 10 or height > 40 or difficulty > 5 or difficulty < 1:
            print("Please choose a number in the range")
            continue
        else: 
            break

    difficulty = float(difficulty / 5.0)
    return width, height, difficulty

# Initialize window with curses
def setup_window(height, width):
    """
    Basic setup of curses and window.
    """
    curses.initscr()
    win = curses.newwin(height, width, 0, 0) 
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(500)

    return win, curses

# Move the ship
def move_ship(win, ship):
	
    event = win.getch()

    x = ship[1]
    # avoid hitting the boundary
    if x > 1 and event == curses.KEY_LEFT:
        x -= 1
    if x < width - 2 and event == curses.KEY_RIGHT:
        x += 1
    prev_ship = ship
    ship = (height - 2, x)
    

    if prev_ship != ship:
        draw_ship(win, prev_ship, ' ')
        draw_ship(win, ship, '^')

    return ship

# generate and update rocks
def update_rock(rocks):

    global score
    #new rock contains exact coordinates of all rocks
    new_rocks = []

    #integer_rock contains rounded coordinates of all the rocks
    integer_rocks = []

    if rocks != []:
        for rock in rocks:
            win.addch(math.floor(rock[0]), rock[1], ' ')
            if math.floor(rock[0]) != height - 2:
                new_rocks.append((rock[0] + 0.05, rock[1]))

    if new_rocks == [] or isclose(new_rocks[0][0], int(new_rocks[0][0])):
        score += 1
        for i in range(num_rock):
            new_rocks.insert(0, (1, randint(1,width-2)))

    for rock in new_rocks:
        integer_rocks.append((math.floor(rock[0]), rock[1]))

    return new_rocks, integer_rocks


def draw_rock(win,rocks):
    for rock in rocks:
        win.addch(math.floor(rock[0]), rock[1], 'O')


def draw_ship(win, ship, symbol):
    try:    
        win.addch(ship[0], ship[1], symbol)
    except curses.error:
        pass


def update_score(win):
    
    if score > height - 2:
        point = score - height + 2
    else:
        point = 0
    win.addstr(0, 2, ' Score: ' + str(point) + ' ')

# after hitted by any rock, show ending
def show_ending(win, ship):
	
    win.addch(ship[0] - 1, ship[1], 'X')

    
    if score > height - 1:
        point = score - height + 1
    else:
        point = 0
    win.addstr(0, 2, ' Final Score: ' + str(point) + '. ' + 
                "(Press ESC to exit)")
    key = curses.KEY_RIGHT
    ESC = 27
    while key != ESC:
        key = win.getch()
# adjust speed with score
def increase_speed(win):
    win.timeout(1000 // (score + height * 2))

if __name__ == '__main__':

    width, height, difficulity = get_initial_input()

    num_rock = math.ceil(width / 6 * difficulity)

    win, curses = setup_window(height,width)

    rocks = []

    ship = (height - 2, width // 2)

    draw_ship(win, ship, '^')

    while True:
        update_score(win)
        increase_speed(win)
        ship = move_ship(win, ship)
        new_rocks, integer_rocks = update_rock(rocks)

        # check if ship crashed
        if ship in integer_rocks:
            draw_rock(win, rocks)
            break

        draw_rock(win, integer_rocks)
        rocks = new_rocks

    show_ending(win, ship)
    curses.endwin()
    

