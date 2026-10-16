import arcade

# must change values
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, style=self.WINDOW_STYLE_BORDERLESS, resizable=True)
        self.background_sprite_list = arcade.SpriteList()
        self.ui_sprite_list = arcade.SpriteList()
        self.write_text_on_terminal_list = arcade.SpriteList()
        
    def setup(self):
        self.CRT_background()
        self.overlay_green_tint()
        self.written_text_on_terminal()

    # s a ocupat geamanu, dracu sa l ia
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

        self.overlay.width = width
        self.overlay.height = height
        self.overlay.position = (width/2, height/2)

    # CRT screen image used as background
    def CRT_background(self):
        self.bg_image = arcade.Sprite("background.jpg")
        self.bg_image.width = 1400
        self.bg_image.height = 1000
        self.bg_image.position = (self.width/2, self.height/2)
        self.bg_image.color = (50, 70, 30)
        self.background_sprite_list.append(self.bg_image)

    # Greenish tint over the background, must change some values
    def overlay_green_tint(self):
        self.overlay = arcade.SpriteSolidColor(self.width, self.height, color=(0, 251, 42, 10))
        self.overlay.position = (self.width/2, self.height/2)
        self.ui_sprite_list.append(self.overlay)

    # just checked how create_text_sprite works, these will be the text lines on the screen
    def written_text_on_terminal(self):
        self.write_text = arcade.create_text_sprite("heheha", arcade.color.WHITE, font_size=12)
        self.write_text_on_terminal_list.append(self.write_text)

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw()
        self.ui_sprite_list.draw()
        self.write_text_on_terminal_list.draw()

if __name__ == "__main__":
    window = GameView()
    window.setup()
    arcade.run()

        

    
