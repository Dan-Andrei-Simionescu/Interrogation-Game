import arcade
import config

class BackgroundManager:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.bg_image = arcade.Sprite(config.SCREEN_PATH)
        self.bg_image.width = 1400
        self.bg_image.height = 1000
        self.bg_image.color = (77, 99, 56)
        self.sprite_list.append(self.bg_image)

    def resize(self, window_width, window_height, target_aspect_ratio):
        if window_width / window_height > target_aspect_ratio:
            new_height = window_height
            new_width = window_height * target_aspect_ratio
        else:
            new_width = window_width
            new_height = window_width / target_aspect_ratio

        new_width = min(new_width, 1400)
        new_height = min(new_height, 1000)

        self.bg_image.width = new_width
        self.bg_image.height = new_height
        self.bg_image.position = (window_width / 2, window_height / 2)

    def draw(self):
        self.sprite_list.draw()