import pyglet as pg
import logging
import os
from board import Board

class Main(pg.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if os.path.exists('log.txt'):
            os.remove('log.txt')
        logging.basicConfig(filename='log.txt', level=logging.INFO)
        
        self.image = pg.image.load('terrain.bmp')
        self.image_x = 0
        self.image_y = 0
        self.scale = 1.0
        self.update_tick = 1/30
        self.background = pg.sprite.Sprite(self.image.get_region(self.image_x, self.image_y, int(self.width / self.scale), int(self.height / self.scale)), subpixel=True)
        
        self.lines = pg.graphics.Batch()
        
        self.board = Board()
        
        pg.clock.schedule_interval(self.update, self.update_tick)

    def update(self, dt):
        self.background.delete()
        self.image_x = max(0, self.image_x)
        self.image_y = max(0, self.image_y)
        self.image_x = int(min(self.image.width - self.width / self.scale, self.image_x))
        self.image_y = int(min(self.image.height - self.height / self.scale, self.image_y))
        self.background = pg.sprite.Sprite(self.image.get_region(self.image_x, self.image_y, int(self.width / self.scale), int(self.height / self.scale)), subpixel=True)
        self.background.scale = self.scale
        
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
        self.image_x -= dx / self.scale
        self.image_y -= dy / self.scale
        self.image_x = max(0, min(self.image.width - self.width / self.scale, self.image_x))
        self.image_y = max(0, min(self.image.height - self.height / self.scale, self.image_y))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        prev_scale = self.scale
        self.scale *= (1.1 ** scroll_y)
        self.scale = max(0.66, self.scale)
        
        center_x = self.width / 2.0 / prev_scale + self.image_x
        center_y = self.height / 2.0 / prev_scale + self.image_y
        
        offset_x = (center_x - self.image_x) * prev_scale
        offset_y = (center_y - self.image_y) * prev_scale
        
        self.image_x = center_x - offset_x / self.scale
        self.image_y = center_y - offset_y / self.scale
        self.image_x = max(0, min(self.image.width - self.width / self.scale, self.image_x))
        self.image_y = max(0, min(self.image.height - self.height / self.scale, self.image_y))

    def on_draw(self):
        self.clear()
        pg.gl.glTexParameteri(pg.gl.GL_TEXTURE_2D, pg.gl.GL_TEXTURE_MAG_FILTER, pg.gl.GL_NEAREST)
        self.background.draw()
        gui.draw_line(self, (0, 0), (self.width, self.height))

if __name__ == "__main__":
    main = Main(resizable=True)
    pg.app.run(1/30)
