import pyglet as pg
import numpy as np

target_fps = 1/15

draw_array = np.vectorize(lambda n: n.draw() if n is not None else None)

get_length = lambda a: np.sum(np.vectorize(lambda n: int(n) if n.isdigit() else 0)(a))

make_lines = np.vectorize(lambda c1, dist_vector, length, scale, i: pg.shapes.Line(c1[0] + dist_vector[0] * (i + 0.1) / length, c1[1] + dist_vector[1] * (i + 0.1) / length, c1[0] + dist_vector[0] * (i + 0.9) / length, c1[1] + dist_vector[1] * (i + 0.9) / length, color=(0, 0, 0), width=5*scale), signature='(2),(2),(),(),()->()')

delete_sprites = np.vectorize(lambda n: n.delete() if n is not None else None)

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

def render_city(main, data):
    coords = data['coords']
    adjusted_x = (coords[0] - main.shift_x) * main.scale
    adjusted_y = (main.image.height - main.shift_y - coords[1]) * main.scale
    if 0 <= adjusted_x < main.width and 0 <= adjusted_y < main.height:
        return np.array([pg.shapes.Circle(adjusted_x, adjusted_y, 5 * main.scale, color=(0, 0, 0)), pg.text.Label(data['name'], x=adjusted_x, y=adjusted_y + 5 * main.scale, anchor_x='center', anchor_y='baseline', font_size=10 * main.scale, color=(0, 0, 0, 255))])
    return np.array([None, None])

render_cities = np.vectorize(render_city, signature='(),()->(n)')

def render_route(main, data):
    data = list(data)[0][2]
    c1 = data['c1']
    c1 = np.array([c1[0] - main.shift_x, main.image.height - main.shift_y - c1[1]]) * main.scale
    c2 = data['c2']
    c2 = np.array([c2[0] - main.shift_x, main.image.height - main.shift_y - c2[1]]) * main.scale
    cost = data['cost']
    if not (c1[0] < 0 or c1[0] >= main.width or c1[1] < 0 or c1[1] >= main.height or c2[0] < 0 or c2[0] >= main.width or c2[1] < 0 or c2[1] >= main.height):
        return create_lines(np.array(c1), np.array(c2), main.scale, cost)
    return np.array([])

render_routes = np.vectorize(render_route, signature='(),()->(n)')
