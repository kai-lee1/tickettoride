import pyglet as pg
import numpy as np

draw_array = np.vectorize(lambda n: n.draw())

def update_background(main):
    main.background.delete()
    main.shift_x = max(0, main.shift_x)
    main.shift_y = max(0, main.shift_y)
    main.shift_x = int(min(main.image.width - main.width / main.scale, main.shift_x))
    main.shift_y = int(min(main.image.height - main.height / main.scale, main.shift_y))
    main.background = pg.sprite.Sprite(main.image.get_region(main.shift_x, main.shift_y, int(main.width / main.scale), int(main.height / main.scale)), subpixel=True)
    main.background.scale = main.scale
