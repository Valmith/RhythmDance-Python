import pgzrun
import os
from random import randint

#Centers the window 
os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

move_list = []
display_list = []

score = 0
current_move = 0
count = 4
dance_length = 4

say_dance = False
show_countdown = True
moves_complete = False
game_over = False

#draws the pictures to the window
dancer = Actor("dancer-start.png")
dancer.pos = CENTER_X + 5, CENTER_Y - 40

up = Actor("up.png")
up.pos = CENTER_X, CENTER_Y + 110
right = Actor("right.png")
right.pos = CENTER_X + 60, CENTER_Y + 170
down = Actor("down.png")
down.pos = CENTER_X, CENTER_Y + 230
left = Actor("left.png")
left.pos = CENTER_X - 60, CENTER_Y + 170

def draw():
    global game_over, score, say_dance
    global count, show_countdown

    if not game_over:
        screen.clear()
        screen.blit("stage.png", (0, 0))
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()
        screen.draw.text("Score: " + str(score), color="black", topleft=(10, 10))

        if say_dance:
            screen.draw.text("Dance!", color="black", topleft=(CENTER_X - 65, 150), fontsize=60)

        if show_countdown:
            screen.draw.text(str(count), color="black", topleft=(CENTER_X - 8, 150), fontsize=60)

    else:
        screen.clear()
        screen.blit("stage", (0, 0))
        screen.draw.text("Score: " + str(score), color="black", topleft=(10, 10))
        screen.draw.text("GAME OVER!", color="black", topleft=(CENTER_X - 130, 220), fontsize=60)

def reset_dancer():
    global game_over
    if not game_over:
        dancer.image = "dancer-start.png"
        up.image = "up.png"
        right.image = "right.png"
        down.image = "down.png"
        left.image = "left.png"
    return

def update_dancer(move):
    global game_over
    if not game_over:
        if move == 0:
            up.image = "up-lit.png"
            dancer.image = "dancer-up.png"
            clock.schedule(reset_dancer, 0.5)
        elif move == 1:
            right.image = "right-lit.png"
            dancer.image = "dancer-right.png"
            clock.schedule(reset_dancer, 0.5)
        elif move == 2:
            down.image = "down-lit.png"
            dancer.image = "dancer-down.png"
            clock.schedule(reset_dancer, 0.5)
        else:
            left.image = "left-lit.png"
            dancer.image = "dancer-left.png"
            clock.schedule(reset_dancer, 0.5)

    return

def display_moves():
    global move_list, display_list, dance_length
    global say_dance, show_countdown, current_move

    if display_list:
        this_move = display_list[0]
        display_list = display_list[1:]

        if this_move == 0:
            update_dancer(0)
            clock.schedule(display_moves, 1)
        elif this_move == 1:
            update_dancer(1)
            clock.schedule(display_moves, 1)
        elif this_move == 2:
            update_dancer(2)
            clock.schedule(display_moves, 1)
        else:
            update_dancer(3)
            clock.schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False
    return

#just the timer
def countdown():
    global count, game_over, show_countdown

    if count > 1:
        count = count - 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()
    return


def generate_moves(): # updated
    global move_list, dance_length, count
    global show_countdown, say_dance

    count = 4
    move_list = []
    say_dance = False

    for move in range(0, dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)

    show_countdown = True
    countdown()

def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:
        current_move = current_move + 1
    else:
        moves_complete = True
    return

#KEY PRESSES to see if right or wrong move
def on_key_up(key):
    global score, game_over, move_list, current_move

    if key == keys.UP:
        update_dancer(0)
        if move_list[current_move] == 0:
            score = score + 1
            next_move()
        else:
            game_over = True

    elif key == keys.RIGHT:
        update_dancer(1)
        if move_list[current_move] == 1:
            score = score + 1
            next_move()
        else:
            game_over = True

    elif key == keys.DOWN:
        update_dancer(2)
        if move_list[current_move] == 2:
            score = score + 1
            next_move()
        else:
            game_over = True

    elif key == keys.LEFT:
        update_dancer(3)
        if move_list[current_move] == 3:
            score = score + 1
            next_move()
        else:
            game_over = True

    return

generate_moves()
music.play("vanishing-horizon")

def update():
    global game_over,current_move, moves_complete
    if not game_over:
        if moves_complete:
            generate_moves()
            moves_complete = False
            current_move = 0

    else:
        music.stop()

pgzrun.go()
