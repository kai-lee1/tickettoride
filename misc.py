import pyglet as pg
import numpy as np

target_fps = 1/15

draw_array = np.vectorize(lambda n: n.draw())

get_length = lambda a: np.sum(np.vectorize(lambda n: int(n) if n.isdigit() else 0)(a))

make_lines = np.vectorize(lambda c1, dist_vector, length, scale, i: pg.shapes.Line(c1[0] + dist_vector[0] * (i + 0.1) / length, c1[1] + dist_vector[1] * (i + 0.1) / length, c1[0] + dist_vector[0] * (i + 0.9) / length, c1[1] + dist_vector[1] * (i + 0.9) / length, color=(0, 0, 0), width=2*scale), signature='(2),(2),(),(),()->()')

def create_lines(c1, c2, scale, cost: str):
    data = np.array(cost.split())
    lines = np.array([])
    length = get_length(data)
    
    dist_vector = c2 - c1
    
    lines = make_lines(c1, dist_vector, length, scale, np.array(range(length)))

    return lines

def update_background(main):
    main.background.delete()
    main.shift_x = max(0, main.shift_x)
    main.shift_y = max(0, main.shift_y)
    main.shift_x = int(min(main.image.width - main.width / main.scale, main.shift_x))
    main.shift_y = int(min(main.image.height - main.height / main.scale, main.shift_y))
    main.background = pg.sprite.Sprite(main.image.get_region(main.shift_x, main.shift_y, int(main.width / main.scale), int(main.height / main.scale)), subpixel=True)
    main.background.scale = main.scale
