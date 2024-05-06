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
        
        self.image: pg.image.AbstractImage = pg.image.load('terrain.bmp')
        self.shift_x = 0
        self.shift_y = 0
        self.scale = 1.0
        self.update_tick = 1/30
        self.background = pg.sprite.Sprite(self.image.get_region(self.shift_x, self.shift_y, int(self.width / self.scale), int(self.height / self.scale)), subpixel=True)
        
        self.lines = np.array([])
        self.cities = np.array([])
        
        self.board = Board()
        
        pg.clock.schedule_interval(self.update, self.update_tick)

    def update(self, dt):
        misc.update_background(self)
        
        for city in self.cities:
            city.delete()
        
        self.cities = np.array([])
            
        for _, data in self.board.network.nodes.items():
            coords = data['coords']
            adjusted_x = (coords[0] - self.shift_x) * self.scale
            adjusted_y = (self.image.height - self.shift_y - coords[1]) * self.scale
            if 0 <= adjusted_x < self.width and 0 <= adjusted_y < self.height:
                self.cities = np.append(self.cities, pg.shapes.Circle(adjusted_x, adjusted_y, 5 * self.scale, color=(0, 0, 0)))
        
        if dt < 1/30:
            pass
        elif dt/self.update_tick > 2:
            self.update_tick *= 1.1
            pg.clock.unschedule(self.update)
            pg.clock.schedule_interval(self.update, self.update_tick)
            self.on_mouse_scroll(0, 0, 0, 1)
        elif dt/self.update_tick < 1.1:
            self.update_tick /= 1.1
            pg.clock.unschedule(self.update)
            pg.clock.schedule_interval(self.update, self.update_tick)

    def on_close(self):
        logging.info("Closing the application")
        pg.app.exit()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.shift_x -= dx / self.scale
        self.shift_y -= dy / self.scale
        self.shift_x = max(0, min(self.image.width - self.width / self.scale, self.shift_x))
        self.shift_y = max(0, min(self.image.height - self.height / self.scale, self.shift_y))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        prev_scale = self.scale
        self.scale *= (1.1 ** scroll_y)
        self.scale = max(0.66, self.scale)
        
        center_x = self.width / 2.0 / prev_scale + self.shift_x
        center_y = self.height / 2.0 / prev_scale + self.shift_y
        
        offset_x = (center_x - self.shift_x) * prev_scale
        offset_y = (center_y - self.shift_y) * prev_scale
        
        self.shift_x = center_x - offset_x / self.scale
        self.shift_y = center_y - offset_y / self.scale
        self.shift_x = max(0, min(self.image.width - self.width / self.scale, self.shift_x))
        self.shift_y = max(0, min(self.image.height - self.height / self.scale, self.shift_y))

    def on_draw(self):
        self.clear()
        pg.gl.glTexParameteri(pg.gl.GL_TEXTURE_2D, pg.gl.GL_TEXTURE_MAG_FILTER, pg.gl.GL_NEAREST)
        self.background.draw()
        if len(self.cities) > 0:
            misc.draw_array(self.cities)

if __name__ == "__main__":
    main = Main(resizable=True)
    pg.app.run(1/30)
