from pico2d import *
import random

from Boy import Boy


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDLK_LEFT or event.type == SDLK_RIGHT or event.type == SDLK_KP_ENTER:
            boy.handle_event(event)


def reset_world():
    global running
    global grass
    global team
    global world
    global boy

    running = True
    world = []


    boy = Boy()
    world.append(boy)
    
    grass = Grass()
    world.append(grass)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.025)

close_canvas()
