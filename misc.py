import pyglet as pg
import numpy as np
import logging

target_fps = 1/15

card_dim = (340, 210)

gui_gap = (0.8, 0.8)

colors = { "L": (75, 0, 130),
            "R": (255, 0, 0),
            "O": (255, 165, 0),
            "Y": (255, 255, 0),
            "G": (0, 128, 0),
            "B": (0, 0, 255),
            "P": (255, 0, 255),
            "U": (0, 0, 0),
            "W": (255, 255, 255)}

def log_and_func(message, func, *args):
    logging.info(message)
    return func(*args)

draw_array = np.vectorize(lambda n: n.draw() if n is not None else None)

get_length = lambda a: np.sum(np.vectorize(lambda n: int(n) if n.isdigit() else 0)(a))

make_lines = np.vectorize(lambda c1, dist_vector, length, scale, i, data: pg.shapes.Line(c1[0] + dist_vector[0] * (i + 0.1) / length, c1[1] + dist_vector[1] * (i + 0.1) / length, c1[0] + dist_vector[0] * (i + 0.9) / length, c1[1] + dist_vector[1] * (i + 0.9) / length, color=colors[data], width=5*scale), signature='(2),(2),(),(),(),()->()')

def delete_help(sprite):
    try:
        sprite.delete()
    except:
        del sprite

delete_sprites = np.vectorize(lambda n: delete_help(n) if n is not None else None)

def create_lines(c1, c2, scale, cost: str):
    data = np.array(cost.split())
    
    dist_vector = c2 - c1
    
    lines = make_lines(c1, dist_vector, len(data), scale, np.array(range(len(data))), data)

    return lines

def update_background(main):
    main.background.delete()
    main.shift_x = max(0, main.shift_x)
    main.shift_y = max(0, main.shift_y)
    main.shift_x = int(min(main.image.width - main.width * gui_gap[0] / main.scale, main.shift_x))
    main.shift_y = int(min(main.image.height - main.height * gui_gap[1] / main.scale, main.shift_y))
    main.background = pg.sprite.Sprite(main.image.get_region(main.shift_x, main.shift_y, int(main.width * gui_gap[0] / main.scale), int(main.height * gui_gap[1] / main.scale)), subpixel=True)
    main.background.scale = main.scale

def render_city(main, data):
    coords = data['coords']
    adjusted_x = (coords[0] - main.shift_x) * main.scale
    adjusted_y = (main.image.height - main.shift_y - coords[1]) * main.scale
    if 0 <= adjusted_x < main.width * gui_gap[0] and 0 <= adjusted_y < main.height * gui_gap[1]:
        return np.array([pg.shapes.Circle(adjusted_x, adjusted_y, 5 * main.scale, color=(0, 0, 0)), pg.text.Label(data['name'], x=adjusted_x, y=adjusted_y + 5 * main.scale, anchor_x='center', anchor_y='baseline', font_size=10 * main.scale, color=(0, 0, 0, 255))])
    return np.array([None, None])

render_cities = np.vectorize(render_city, signature='(),()->(n)')

def render_route(main, data):
    data = list(data)[2]
    c1 = data['c1']
    c1 = np.array([c1[0] - main.shift_x, main.image.height - main.shift_y - c1[1]]) * main.scale
    c2 = data['c2']
    c2 = np.array([c2[0] - main.shift_x, main.image.height - main.shift_y - c2[1]]) * main.scale
    cost = data['cost']
    if not (c1[0] < 0 or c1[0] >= main.width * gui_gap[0] or c1[1] < 0 or c1[1] >= main.height * gui_gap[1] or c2[0] < 0 or c2[0] >= main.width * gui_gap[0] or c2[1] < 0 or c2[1] >= main.height * gui_gap[1]):
        #logging.info(create_lines(np.array(c1), np.array(c2), main.scale, cost))
        return create_lines(np.array(c1), np.array(c2), main.scale, cost)
    return None

render_routes = np.vectorize(render_route, signature='(),(3)->()')

# def render_card(main, x, y, scale, key):
#     img = main.cards_images[key]
#     card = pg.sprite.Sprite(img.get_region(0, 0, *card_dim))
#     card.x = x
#     card.y = y
#     card.scale = scale
#     main.cards = np.append(main.cards, card)
#     logging.info(f"Card rendered with vertexes {card._vertex_list}")

def render_face_up(main):
    if main.cards.size > 0:
        delete_sprites(main.cards)
    
    main.cards = np.array([])
    
    for i in range(4, -1, -1):
        main.cards = np.append(main.cards, pg.shapes.Rectangle(main.width * gui_gap[0] / 5 * i, main.height * gui_gap[1], main.width * gui_gap[0] / 5, main.height * (1 - gui_gap[1]), color=colors[main.board.face_up[i]]))
        # render_card(main, i * (main.width * gui_gap[0] - card_dim[0] * (main.height * (1 - gui_gap[1])) / card_dim[1]) / 4, main.height * gui_gap[1], (main.height * (1 - gui_gap[1])) / card_dim[1], main.board.face_up[i])

def render_side_bar(main):
    if len(main.side_bar_components) > 0:
        delete_sprites(list(main.side_bar_components.values()))
    
    main.side_bar_components = dict()
    
    main.side_bar_components["background"] = pg.shapes.Rectangle(main.width * gui_gap[0], 0, main.width * (1 - gui_gap[0]), main.height, color=(217, 139, 70))
    main.side_bar_components["button"] = pg.shapes.Rectangle(main.width * gui_gap[0], 0, main.width * (1 - gui_gap[0]) * 0.5, main.height * gui_gap[1] * 0.2, color=(0, 255, 0))
    main.side_bar_components["text"] = pg.text.Label("Draw", x=main.width * gui_gap[0] + main.width * (1 - gui_gap[0]) * 0.25, y=main.height * gui_gap[1] * 0.1, anchor_x='center', anchor_y='center', font_name='Times New Roman', font_size=12, color=(0, 0, 0, 255))
    main.side_bar_components["scoredisplay"] = pg.text.Label(f"P1 Score: {main.board.players[0].score}", x=main.width * gui_gap[0] + main.width * (1 - gui_gap[0]) * 0.5, y=main.height * gui_gap[1] * 0.4, anchor_x='center', anchor_y='center', font_name='Times New Roman', font_size=12, color=(0, 0, 0, 255))
    main.side_bar_components["scoredisplay2"] = pg.text.Label(f"P2 Score: {main.board.players[1].score}", x=main.width * gui_gap[0] + main.width * (1 - gui_gap[0]) * 0.5, y=main.height * gui_gap[1] * 0.3, anchor_x='center', anchor_y='center', font_name='Times New Roman', font_size=12, color=(0, 0, 0, 255))
    #main.side_bar_components["end turn label"] = pg.text.Label("End your turn", x=main.width * gui_gap[0] + main.width * (1 - gui_gap[0]) * 0.5, y=main.height * gui_gap[1] * 0.2, anchor_x='center', anchor_y='center', font_name='Times New Roman', font_size=12, color=(0, 0, 0, 255))

    player1_hand = main.board.players[0].hand
    card_width = main.width * (1 - gui_gap[0]) * 0.1
    card_height = main.height * gui_gap[1] * 0.2
    for i, card in enumerate(player1_hand):
        card_x = main.width * gui_gap[0] + i * card_width * 0.4
        card_y = main.height * gui_gap[1] * 0.6
        main.side_bar_components[f"card_{i}"] = pg.shapes.Rectangle(card_x, card_y, card_width, card_height, color=colors[card])


        #Render small boxes for each unique color in player 1's hand
    # player1_hand = main.board.players[0].hand
    # unique_colors = set(player1_hand)
    # box_width = main.width * (1 - gui_gap[0]) * 0.1
    # box_height = main.height * gui_gap[1] * 0.2
    # for i, color in enumerate(unique_colors):
    #     box_x = main.width * gui_gap[0] + i * box_width
    #     box_y = main.height * gui_gap[1] * 0.6
    #     main.side_bar_components[f"box_{color}"] = pg.shapes.Rectangle(box_x, box_y, box_width, box_height, color=colors[color])
    #     color_count = player1_hand.len(color)
    #     for color in :
    #         if ()
    #     main.side_bar_components[f"label_{color}"] = pg.text.Label(str(color_count), x=box_x + box_width / 2, y=box_y + box_height / 2, anchor_x='center', anchor_y='center', font_name='Times New Roman', font_size=12, color=(0, 0, 0, 255))
