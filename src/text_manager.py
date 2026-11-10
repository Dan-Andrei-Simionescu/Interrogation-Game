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

    def setup(self, bg_width):
        # self.message = (
        #     "  1  [||||||||||||||||||||||||93.1%]   Tasks: 140, 212 thr; 2 running\n"
        #     "  2  [||||||||||             34.0%]   Load average: 1.05 1.12 1.15\n"
        #     "  3  [|||||||||||||||||      61.4%]   Uptime: 14 days, 03:22:15\n"
        #     "  4  [|||||                   8.2%]\n"
        #     "  Mem[|||||||||||||||||1.83G/7.76G]\n"
        #     "  Swp[|                  21M/2.00G]\n"
        #     "\n"
        #     "  PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command\n"
        #     " 1354 root       20   0 1342M  141M 82252 S 34.0  1.8 14h31:12 /usr/bin/dockerd\n"
        #     " 2791 dasduke    20   0 4814M  312M 14210 R 22.4  4.0  2:14.33 python3 main.py\n"
        #     "  983 root       20   0  541M 64320 38142 S  8.2  0.8 10:14.02 /usr/lib/xorg/Xorg\n"
        #     " 1412 dasduke    20   0 2145M  210M  4120 S  2.0  2.6  1h12:45 gnome-shell\n"
        #     " 3125 dasduke    20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        #     "    1 root       20   0  168M 11200  8100 S  0.0  0.1  0:12.44 /sbin/init\n"
        #     "  512 root       20   0  112M  4200  2100 S  0.0  0.0  0:04.10 /sbin/syslogd\n"
        #     "   67 dasduke    20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        #     " 2233 other      20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        #     " 8923 dasduke    20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        #     " 1236 dasduke    20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        #     " 2324 dasduke    20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        #     "   11 root       20   0  812M 43110 11024 S  1.5  0.5  0:00.12 /bin/bash\n"
        # )

        for i in range(3):
            if i == 0:
                # raw_message = newstext()
                pass
            elif i == 1:
                # raw_message = dialoguetext()
                pass
            else:
                # raw_message = optionstext()
                pass

            self.message = "\n".join(
                textwrap.fill(line, width=80, subsequent_indent="   ")
                for line in raw_message.splitlines()
            )

            self.write_command_line = arcade.Text("", 0, 0, color=(60, 180, 40), width=20000, font_name=config.FONT_NAME, font_size=20, anchor_y="top", multiline=True)
            self.count_letter = 0
            arcade.schedule(self.add_letter, 0.025)

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