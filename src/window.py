import arcade
import textwrap
from arcade.gl import geometry

# must change values
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, style=self.WINDOW_STYLE_BORDERLESS, resizable=True)
        self.background_sprite_list = arcade.SpriteList()
        self.ui_sprite_list = arcade.SpriteList()

        # GL Shader
        vertex_shader = """
            #version 330
            in vec2 in_vert;
            in vec2 in_uv;
            out vec2 v_uv;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                v_uv = in_uv;
            }
        """

        # GL Shader for curved screen effect
        fragment_shader = """
            #version 330
            uniform sampler2D texture0;
            in vec2 v_uv;
            out vec4 f_color;

            void main() {
                // CRT curve effect
                vec2 uv = v_uv * 2.0 - 1.0;
                float curvature = 0.15; 
                uv += uv * dot(uv, uv) * curvature;
                uv = uv * 0.5 + 0.5;

                // Pixelized screen style
                float pixel_size = 0.001; 
                
                // Screen size
                vec2 resolution = vec2(1400.0, 1000.0); 
                
                // aproximate coordonates for rounded like pixels
                vec2 pixelated_uv = floor(uv * (resolution / pixel_size)) / (resolution / pixel_size);

                // check edges with distorted coords but draw pixelized coords.
                if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
                    f_color = vec4(0.0, 0.0, 0.0, 1.0); // Margini negre
                } else {
                    f_color = texture(texture0, pixelated_uv); // Aplicăm textura pixelată
                    
                    // Horizontal lines effect
                    // float scanline = sin(uv.y * 800.0) * 0.04;
                    // f_color.rgb -= scanline;
                }
            }
        """
        
        # Compiles program and creates a 2D interface where we apply texture
        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.quad_fs = geometry.quad_2d_fs()
        
        # Frame Buffer for distortion effect
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), components=4)]
        )
    
    def setup(self):
        arcade.load_font("Perfect DOS VGA 437.ttf")
        self.CRT_background()
        # self.overlay_green_tint()
        self.write_text()

    # resize background photo when window is minimized
    def on_resize(self, width, height):
        super().on_resize(width, height)

        self.target_aspect_ratio = 1400/1000

        if width / height > self.target_aspect_ratio:
            new_height = height
            new_width = height * self.target_aspect_ratio
        else:
            new_width = width
            new_height = width/self.target_aspect_ratio

        new_width = min(new_width, 1400)
        new_height = min(new_height, 1000)

        self.bg_image.width = new_width
        self.bg_image.height = new_height
        self.bg_image.position = (width/2, height/2)

        # self.overlay.width = width
        # self.overlay.height = height
        # self.overlay.position = (width/2, height/2)

        self.update_text_position(width, height)

        # redo frame buffer texture for every resizing of the screen
        if width > 0 and height > 0:
            self.fbo = self.ctx.framebuffer(
                color_attachments=[self.ctx.texture((width, height), components=4)]
            )

    def update_text_position(self, width, height):
        bg_image_left_edge = ((width / 2) - (self.bg_image.width / 2))
        bg_image_top_edge = ((height / 2) + (self.bg_image.height / 2))

        padding_x = 100 * (self.bg_image.width / 1400)
        padding_y = 120 * (self.bg_image.height / 1000)

        self.write_command_line.x = bg_image_left_edge + padding_x
        self.write_command_line.y = bg_image_top_edge - padding_y

        # self.write_command_line.width = self.bg_image.width - (padding_x * 2)

        self.write_command_line.font_size = 20 * self.bg_image.width / 1400

    # CRT screen image used as background
    def CRT_background(self):
        self.bg_image = arcade.Sprite("CRT_ScreenV2.jpeg")
        self.bg_image.width = 1400
        self.bg_image.height = 1000
        self.bg_image.position = (self.width/2, self.height/2)
        self.bg_image.color = (77, 99, 56)
        self.background_sprite_list.append(self.bg_image)

    # Greenish tint over the background, must change some values
    # def overlay_green_tint(self):
    #     self.overlay = arcade.SpriteSolidColor(self.width, self.height, color=(0, 251, 42, 10))
    #     self.overlay.position = (self.width/2, self.height/2)
    #     self.ui_sprite_list.append(self.overlay)

    # Written text on screen logic
    def write_text(self):
        raw_message = " Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi!" \
        " Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi!" \
        " Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi! Buna, Cartita si Gabi!"
        self.message = textwrap.fill(raw_message, width=80)
        self.write_command_line = arcade.Text("", 0, 0, color=(60, 180, 100), width=self.bg_image.width, font_name="Perfect DOS VGA 437", font_size=20, anchor_y="top", multiline=True)
        self.count_letter = 0
        arcade.schedule(self.add_letter, 0.025)

    def add_letter(self, delta_time: float):
        if self.count_letter <= len(self.message):
            self.write_command_line.text = self.message[:self.count_letter]
            self.count_letter += 1
        else:
            arcade.unschedule(self.add_letter)


    def on_draw(self):
        # Draw on the Frame Buffer
        self.fbo.use()
        self.fbo.clear(color=arcade.color.BLACK)

        self.background_sprite_list.draw()
        # self.ui_sprite_list.draw()
        self.write_command_line.draw()

        # Return to the main screen
        self.ctx.screen.use()
        self.clear()

        # Draw generated texture on screen, using the distortion shader
        self.fbo.color_attachments[0].use(0)
        self.quad_fs.render(self.program)


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()