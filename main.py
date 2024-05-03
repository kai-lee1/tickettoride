import pyglet as pg
import logging
import os

window = pg.window.Window(resizable=True)

if os.path.exists('log.txt'):
    os.remove('log.txt')

logging.basicConfig(filename='log.txt', level=logging.INFO)

# Load the image
image: pg.image.AbstractImage = pg.image.load('terrain.bmp')

image_x = 0
image_y = 0
scale = 1.0  # Initial scale factor

update_tick = 1/30

background = pg.sprite.Sprite(image.get_region(image_x, image_y, int(window.width / scale), int(window.height / scale)))

def update(dt):
    global background, image_x, image_y, update_tick
    background.delete()
    
    image_x = max(0, image_x)
    image_y = max(0, image_y)
    image_x = int(min(image.width - window.width / scale, image_x))
    image_y = int(min(image.height - window.height / scale, image_y))
    
    background = pg.sprite.Sprite(image.get_region(image_x, image_y, int(window.width / scale), int(window.height / scale)))
    background.scale = scale
    
    if dt/update_tick > 2:
        update_tick *= 2
        pg.clock.unschedule(update)
        pg.clock.schedule_interval(update, update_tick)
    
    elif dt/update_tick < 1.1:
        update_tick /= 2
        pg.clock.unschedule(update)
        pg.clock.schedule_interval(update, update_tick)
    
    logging.info(f"Update: {dt/update_tick}")

@window.event
def on_close():
    logging.info("Closing the application")
    pg.app.exit()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global image_x, image_y
    image_x -= dx / scale
    image_y -= dy / scale
    
    # Ensure image stays within bounds
    image_x = max(0, min(image.width - window.width / scale, image_x))
    image_y = max(0, min(image.height - window.height / scale, image_y))

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scale, image_x, image_y
    scale += scroll_y * 0.1
    scale = max(0.5, min(2.0, scale))
    
    # Ensure image stays within bounds
    image_x = max(0, min(image.width - window.width / scale, image_x))
    image_y = max(0, min(image.height - window.height / scale, image_y))

@window.event
def on_draw():
    window.clear()
    pg.gl.glTexParameteri(pg.gl.GL_TEXTURE_2D, pg.gl.GL_TEXTURE_MAG_FILTER, pg.gl.GL_NEAREST)
    background.draw()

pg.clock.schedule_interval(update, update_tick)

pg.app.run()
