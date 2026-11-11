import arcade
import textwrap
import config

from text_level.txt_game_logic import populate_list

class TextManager:
    def __init__(self):
        arcade.load_font(config.FONT_PATH)
        self.write_command_line = None
        self.message = ""
        self.count_letter = 0
        
        self.text_list = None
        self.current_node = None

    def setup(self, bg_width):
        self.text_list = populate_list()
        self.current_node = self.text_list.head

        self.write_command_line = arcade.Text(
            "", 0, 0, 
            color=(60, 180, 40),
            width=20000,
            font_name=config.FONT_NAME, 
            font_size=20, 
            anchor_y="top", 
            multiline=True
        )
        
        self.load_current_text()

    def load_current_text(self):
        if self.current_node is None:
            raw_message = "No more encounters."
        else:
            raw_message = self.current_node.content
        
        self.message = "\n".join(
            textwrap.fill(line, width=80, subsequent_indent="   ")
            for line in raw_message.splitlines()
        )

        self.write_command_line.text = ""
        self.count_letter = 0
        arcade.unschedule(self.add_letter) 
        arcade.schedule(self.add_letter, 0.025)

    def advance_text(self):
        """Called by window.py when the user presses Enter."""
        if self.count_letter < len(self.message):
            self.count_letter = len(self.message)
            self.write_command_line.text = self.message
            arcade.unschedule(self.add_letter)
            return

        if self.current_node is not None:
            self.current_node = self.current_node.next
            
        self.load_current_text()

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