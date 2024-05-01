import pyglet as pg

window = pg.window.Window()


# Load the image
image: pg.image.AbstractImage = pg.image.load('tickettoride/terrain.bmp')

image_x = 0
image_y = 0
scale = 1.0  # Initial scale factor

background = pg.sprite.Sprite(image.get_region(image_x, image_y, int(window.width / scale), int(window.height / scale)))

def update(dt):
    global background, image_x, image_y
    background.delete()
    
    image_x = max(0, image_x)
    image_y = max(0, image_y)
    image_x = int(min(image.width - window.width / scale, image_x))
    image_y = int(min(image.height - window.height / scale, image_y))
    
    background = pg.sprite.Sprite(image.get_region(image_x, image_y, int(window.width / scale), int(window.height / scale)))
    background.scale = scale

@window.event
def on_draw():
    window.clear()
    background.draw()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global image_x, image_y

    # Check if left mouse button is pressed
    if buttons == pg.window.mouse.LEFT:
        # Update the image position based on the mouse movement
        image_x -= dx / scale
        image_y -= dy / scale

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scale

    # Update the scale factor based on the scroll direction
    if scroll_y > 0:
        scale *= 1.1  # Increase scale by 10%
    else:
        scale /= 1.1  # Decrease scale by 10%
    
    scale = max(0.66, scale)  # Prevent scale from going below 1.0

pg.clock.schedule_interval(update, 1/30)

pg.app.run()
