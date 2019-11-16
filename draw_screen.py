'''Draw class implementation for e-paper desk assisstant'''

# import sys picdir =
# os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
# 'pic') libdir =
# os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
# 'lib') if os.path.exists(libdir): sys.path.append(libdir)

import os
import time
from datetime import datetime
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
# from lib.waveshare_epd import epd7in5

# XXX Set to desired system font or font from ./pic/
# Recommended to use monospace font to ensure alignment shape and text
# alignment
# FreeMonoBold18: 11x18 pixels per char
font18 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMonoBold.otf", 18)
# FreeMonoBold24: 15x24 pixels per char
font24 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMonoBold.otf", 24)

WIDTH = 640
HEIGHT = 384

WEEKDAYS = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun"
}

# draw = ImageDraw.Draw(img)

# draw.text((20, 5), WEEKDAYS[today.weekday()], font=font18, fill=0)
# draw.ellipse([(20, 24), (53, 57)], fill=0, outline=0)
# draw.text((21.5, 28.5), f'{today.day}', font=font24, fill=255)

# TODO comment out when running on pi
# img.show()

# TODO uncomment for actual display
# epd.display(epd.getbuffer(img))
# time.sleep(2)
# epd.Clear()
# time.sleep(2)
# epd.sleep()

class Draw:
    '''Draw class to simplify displaying calendar information'''
    def __init__(self):
        # self.epd = epd7in5.EPD()
        # self.epd.init()
        # self.epd.Clear()

        # 255 -> set image to all white
        # 0   -> set image to all black
        self.screen = Image.new('1', (WIDTH, HEIGHT), 255)
        self.font18 = ImageFont.truetype(
            "/usr/share/fonts/opentype/freefont/FreeMonoBold.otf", 18)
        self.font24 = ImageFont.truetype(
            "/usr/share/fonts/opentype/freefont/FreeMonoBold.otf", 24)
        self.draw_screen = ImageDraw.Draw(self.screen)

    def show_away(self) -> None:
        '''Setup display to show away screen'''

    def show_calendar(self) -> None:
        '''Setup display to show calendar'''
        # setup date in upper left corner
        # self.draw_screen.text((70, 5), WEEKDAYS[today.weekday()],
        #                       font=self.font18, fill=0)
        # self.draw_screen.ellipse([(70, 24), (103, 57)], fill=0, outline=0)
        # self.draw_screen.text((71.5, 28.5), f'{today.day}', font=self.font24,
        #                       fill=255)

        today = datetime.today()
        # setup time grid for day
        date_line: float = 65
        grid_width: float = (WIDTH - 10) - date_line
        day_width: float = grid_width / 3

        time_line: float = 60
        grid_height: float = (HEIGHT - 10) - time_line
        time_height: float = grid_height / 5

        for i in range(3):
            self.draw_screen.line([(date_line, 60),
                                   (date_line, (HEIGHT - 10))], fill=0)
            self.draw_screen.text(((date_line + 5), 5),
                                  WEEKDAYS[(today.weekday() + i) % 7],
                                  font=self.font18, fill=0)
            self.draw_screen.ellipse([((date_line + 5), 24),
                                      ((date_line + 38), 57)],
                                     fill=0,
                                     outline=0)
            self.draw_screen.text(((date_line + 6.5), 28.5),
                                  f'{today.day + i}',
                                  font=self.font24, fill=255)

            date_line += day_width

        self.draw_screen.line([(date_line, 60),
                               (date_line, (HEIGHT - 10))], fill=0)

        current_hour, current_minute = get_initial_time(today)
        while time_line < HEIGHT:
            self.draw_screen.line([(60, time_line),
                                   ((WIDTH - 10), time_line)], fill=0)
            self.draw_screen.text((6, (time_line - 9)),
                                  f'{current_hour:02}:{current_minute:02}',
                                  fill=0, font=self.font18)
            current_minute += 30
            if current_minute == 60:
                current_minute = 0
                current_hour += 1

            time_line += time_height

    def display(self) -> None:
        '''Send image to display'''
        # TODO comment out when running on pi
        self.screen.show()

        # TODO uncomment for actual display
        # self.epd.display(self.epd.getbuffer(self.screen))
        # time.sleep(2)
        # self.epd.sleep()

    def add_event(self, event) -> None:
        '''Add event to calendar
        event: to be added to screen
        '''
        # TODO figure out how events will be structured
        # even = dict:
        #       title
        #       time
        #       name
        #       location
        #       privacy


def get_initial_time(today: datetime) -> Tuple[int, int]:
    '''Get initial time set to most recent 30 minute mark'''
    closest_interval: int = (today.minute // 10) * 10
    if closest_interval > 30:
        closest_interval = 30
    else:
        closest_interval = 0

    return (today.hour, closest_interval)


def main():
    '''Demo main function to show default displays'''
    screen_controller = Draw()
    screen_controller.show_calendar()
    screen_controller.display()


if __name__ == '__main__':
    main()
