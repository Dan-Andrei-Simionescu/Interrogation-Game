import arcade
from arcade.gl import geometry

from OpenGL_features import OpenGL_feat
import config
from background_manager import BackgroundManager
from text_manager import TextManager

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, style=self.WINDOW_STYLE_BORDERLESS, resizable=True)
        
        self.target_aspect_ratio = 1400 / 1000
        
        self.background_manager = BackgroundManager()
        self.text_manager = TextManager()

        vertex_shader, fragment_shader = OpenGL_feat()
        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.quad_fs = geometry.quad_2d_fs()
        
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), components=4)]
        )
    
    def setup(self):
        self.background_manager.resize(self.width, self.height, self.target_aspect_ratio)
        self.text_manager.setup(self.background_manager.bg_image.width)
        
        self.text_manager.update_position(
            self.width, 
            self.height, 
            self.background_manager.bg_image.width, 
            self.background_manager.bg_image.height
        )

    def on_resize(self, width, height):
        super().on_resize(width, height)

        self.background_manager.resize(width, height, self.target_aspect_ratio)
        
        bg = self.background_manager.bg_image
        self.text_manager.update_position(width, height, bg.width, bg.height)

        if width > 0 and height > 0:
            self.fbo = self.ctx.framebuffer(
                color_attachments=[self.ctx.texture((width, height), components=4)]
            )

    def on_draw(self):
        self.fbo.use()
        self.fbo.clear(color=(0, 0, 0, 0))
        self.text_manager.draw()

        self.ctx.screen.use()
        self.clear()

        self.background_manager.draw()
        self.ctx.enable(self.ctx.BLEND)
        
        self.fbo.color_attachments[0].use(0)
        self.quad_fs.render(self.program)