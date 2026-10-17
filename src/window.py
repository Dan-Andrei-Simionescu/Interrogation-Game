import arcade

# must change values
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, style=self.WINDOW_STYLE_BORDERLESS, resizable=True)
        self.background_sprite_list = arcade.SpriteList()
        self.ui_sprite_list = arcade.SpriteList()
        
    def setup(self):
        self.CRT_background()
        self.overlay_green_tint()
        self.write_text()

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

        self.update_text_position(width, height)

    def update_text_position(self, width, height):
        bg_image_left_edge = ((width / 2) - (self.bg_image.width / 2))
        bg_image_top_edge = ((height / 2) + (self.bg_image.height / 2))

        padding_x = 100 * (self.bg_image.width / 1400)
        padding_y = 120 * (self.bg_image.height / 1000)

        self.write_command_line.x = bg_image_left_edge + padding_x
        self.write_command_line.y = bg_image_top_edge - padding_y

        self.write_command_line.width = self.bg_image.width - (padding_x * 2)

        self.write_command_line.font_size = 20 * self.bg_image.width / 1400

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

    # Must work here, the written text logic must be inside on_resize, so that it can be seen
    def write_text(self):
        self.message = "Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!" \
        "Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!" \
        "Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!" \
        "Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!Ohaio, minasan!"
        self.write_command_line = arcade.Text("", 0, 0, arcade.color.WHITE, width=self.bg_image.width, font_size=20, anchor_y="top", multiline=True)
        self.count_letter = 0
        arcade.schedule(self.add_letter, 0.05)

    def add_letter(self, delta_time: float):
        if self.count_letter <= len(self.message):
            self.write_command_line.text = self.message[:self.count_letter]
            self.count_letter += 1
        else:
            arcade.unschedule(self.add_letter)


    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw()
        self.ui_sprite_list.draw()

        self.write_command_line.draw()


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

        

    
