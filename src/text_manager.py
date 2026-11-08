import arcade
import textwrap
import config

class TextManager:
    def __init__(self):
        arcade.load_font(config.FONT_PATH)
        self.write_command_line = None
        self.message = ""
        self.count_letter = 0

    def setup(self, bg_width):
        raw_message = " Buna, Cartita si Gabi! " * 24        
        self.message = textwrap.fill(raw_message, width=80)

        self.write_command_line = arcade.Text("", 0, 0, color=(60, 180, 100), width=20000, font_name=config.FONT_NAME, font_size=20, anchor_y="top", multiline=True)
        self.count_letter = 0
        arcade.schedule(self.add_letter, 0.0025)

    def add_letter(self, delta_time: float):
        if self.count_letter <= len(self.message):
            self.write_command_line.text = self.message[:self.count_letter]
            self.count_letter += 1
        else:
            arcade.unschedule(self.add_letter)

    def update_position(self, window_width, window_height, bg_width, bg_height):
        if not self.write_command_line:
            return

        bg_image_left_edge = (window_width / 2) - (bg_width / 2)
        bg_image_top_edge = (window_height / 2) + (bg_height / 2)

        padding_x = 100 * (bg_width / 1400)
        padding_y = 120 * (bg_height / 1000)

        self.write_command_line.x = bg_image_left_edge + padding_x
        self.write_command_line.y = bg_image_top_edge - padding_y

        self.write_command_line.font_size = 20 * (bg_width / 1400)

    def draw(self):
        if self.write_command_line:
            self.write_command_line.draw()