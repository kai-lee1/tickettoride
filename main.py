import pyglet as pg
import numpy as np
import logging
import os
from board import Board
import misc

class Main(pg.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if os.path.exists('log.txt'):
            os.remove('log.txt')
        logging.basicConfig(filename='log.txt', level=logging.INFO)
        
        self.image: pg.image.AbstractImage = pg.image.load('assets/blank.bmp')
        self.cards_images: dict =  {"L": pg.image.load('assets/locomotive.png'), 
                            "R": pg.image.load('assets/red.png'),
                            "O": pg.image.load('assets/orange.png'),
                            "Y": pg.image.load('assets/yellow.png'),
                            "G": pg.image.load('assets/green.png'),
                            "B": pg.image.load('assets/blue.png'),
                            "P": pg.image.load('assets/purple.png'),
                            "U": pg.image.load('assets/black.png'),
                            "W": pg.image.load('assets/white.png')}
        self.shift_x = 0
        self.shift_y = 0
        self.scale = 1.0
        self.update_tick = misc.target_fps
        self.background = pg.sprite.Sprite(self.image.get_region(self.shift_x, self.shift_y, int(self.width * misc.gui_gap[0] / self.scale), int(self.height * misc.gui_gap[1] / self.scale)), subpixel=True)
        
        self.cards = np.array([])
        self.routes = np.array([])
        self.cities = np.array([[None, None]], ndmin=2)
        self.side_bar_components = dict()
        
        self.current_screen = "main"
                
        self.board = Board()
                
        pg.clock.schedule_interval(self.update, self.update_tick)

    def update(self, dt):
        misc.update_background(self)
        
        if self.cities[0][0] is not None:
            misc.delete_sprites(self.cities[:,0])
            misc.delete_sprites(self.cities[:,1])
        
        if self.routes.size > 0:
            misc.delete_sprites(self.routes)
        
        self.cities = np.array([[None, None]], ndmin=2)
        
        self.routes = np.array([])
                
        self.cities = misc.render_cities(self, list(dict(self.board.network.nodes.data()).values()))

        self.routes = np.hstack(misc.render_routes(self, list(self.board.network.edges.data())))
        
        misc.render_face_up(self)
        
        misc.render_side_bar(self)
        
        if dt < misc.target_fps:
            pass
        elif dt/self.update_tick > 2:
            self.update_tick *= 1.1
            pg.clock.unschedule(self.update)
            pg.clock.schedule_interval(self.update, self.update_tick)
        elif dt/self.update_tick < 1.1:
            self.update_tick /= 1.1
            pg.clock.unschedule(self.update)
            pg.clock.schedule_interval(self.update, self.update_tick)
        
        #logging.info(f"Update tick: {1/dt}")

    def on_close(self):
        logging.info("Closing the application")
        pg.app.exit()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.shift_x -= dx / self.scale
        self.shift_y -= dy / self.scale
        self.shift_x = max(0, min(self.image.width - self.width * misc.gui_gap[0] / self.scale, self.shift_x))
        self.shift_y = max(0, min(self.image.height - self.height * misc.gui_gap[1] / self.scale, self.shift_y))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        prev_scale = self.scale
        self.scale *= (1.1 ** scroll_y)
        self.scale = max(0.66, min(self.scale, 3.0))
        
        center_x = self.width * misc.gui_gap[0] / 2.0 / prev_scale + self.shift_x
        center_y = self.height * misc.gui_gap[1] / 2.0 / prev_scale + self.shift_y
        
        offset_x = (center_x - self.shift_x) * prev_scale
        offset_y = (center_y - self.shift_y) * prev_scale
        
        self.shift_x = center_x - offset_x / self.scale
        self.shift_y = center_y - offset_y / self.scale
        self.shift_x = max(0, min(self.image.width - self.width * misc.gui_gap[0] / self.scale, self.shift_x))
        self.shift_y = max(0, min(self.image.height - self.height * misc.gui_gap[1] / self.scale, self.shift_y))

    def on_draw(self):
        self.clear()
        if self.current_screen == "main":
            pg.gl.glTexParameteri(pg.gl.GL_TEXTURE_2D, pg.gl.GL_TEXTURE_MAG_FILTER, pg.gl.GL_NEAREST)
            self.background.draw()
            if self.routes.size > 0:
                misc.draw_array(self.routes)
            misc.draw_array(self.cities[:,0])
            misc.draw_array(self.cities[:,1])
            if self.cards.size > 0:
                misc.draw_array(self.cards)
            if len(self.side_bar_components) > 0:
                misc.draw_array(list(self.side_bar_components.values()))

    def on_mouse_press(self, x, y, button, modifiers):
        for city in self.cities:
            if city[0] is not None:
                if (x,y) in city[0]:
                    break
        for route in self.routes:
            if route is not None:
                if (x,y) in route:
                    break
        if (x, y) in self.side_bar_components["button"]:
            logging.info("Button pressed")
            self.board.players[turn].draw_card() #TODO doesnt work yet

if __name__ == "__main__":
    main = Main(resizable=True)
    pg.clock.schedule_interval(main.update, misc.target_fps)
    pg.app.run()
