'''Draw class implementation for e-paper desk assisstant'''

# import sys picdir =
# os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
# 'pic') libdir =
# os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
# 'lib') if os.path.exists(libdir): sys.path.append(libdir)

import os
import time
import datetime

from PIL import Image, ImageDraw, ImageFont
from lib.waveshare_epd import epd7in5

# picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

# font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
# font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

# XXX Set to desired system font or font from ./pic/

# Recommended to use monospace font to ensure alignment shape and text
# alignment

# FreeMonoBold18: 11x18 pixels per char
font18 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMonoBold.otf", 18)

# FreeMonoBold24: 15x24 pixels per char
font24 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMonoBold.otf", 24)

# epd = epd7in5.EPD()
# epd.init()
# epd.Clear()

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

# img = Image.new('1', (WIDTH, HEIGHT), 255)  # 255 -> set image to all white
# img = Image.new('1', (epd.width, epd.height), 0)
# 255 -> set image to all white
# 0   -> set image to all black

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
        self.epd = epd7in5.EPD()
        self.epd.init()
        self.epd.Clear()

        self.screen = Image.new('1', (WIDTH, HEIGHT), 255)
        self.font18 = ImageFont.truetype("/usr/share/fonts/opentype/freefont/FreeMonoBold.otf", 18)
        self.font24 = ImageFont.truetype("/usr/share/fonts/opentype/freefont/FreeMonoBold.otf", 24)
        self.draw_screen = ImageDraw.Draw(self.screen)


    def show_away(self):
        '''Setup display to show away screen'''

    def show_calendar(self):
        '''Setup display to show calendar'''
        # setup date in upper left corner
        today = datetime.date.today()
        self.draw_screen.text((70, 5), WEEKDAYS[today.weekday()], font=self.font18,
                              fill=0)
        self.draw_screen.ellipse([(70, 24), (103, 57)], fill=0,
                                 outline=0)
        self.draw_screen.text((71.5, 28.5), f'{today.day}', font=self.font24,
                              fill=255)

        # setup time grid for day
        self.draw_screen.line([(65, 60), (65, HEIGHT)], fill=0)
        self.draw_screen.line([(200, 60), (200, HEIGHT)], fill=0)

        self.draw_screen.line([(60, 60), (200, 60)], fill=0)
        self.draw_screen.line([(60, 110), (200, 110)], fill=0)
        self.draw_screen.line([(60, 160), (200, 160)], fill=0)
        self.draw_screen.line([(60, 210), (200, 210)], fill=0)
        self.draw_screen.line([(60, 260), (200, 260)], fill=0)

        self.draw_screen.text((16, 51), '9:00', fill=0, font=self.font18)
        self.draw_screen.text((16, 101), '9:30', fill=0, font=self.font18)
        self.draw_screen.text((6, 151), '10:00', fill=0, font=self.font18)
        self.draw_screen.text((6, 201), '10:30', fill=0, font=self.font18)
        self.draw_screen.text((6, 251), '11:00', fill=0, font=self.font18)

    def display(self):
        '''Send image to display'''
        # TODO comment out when running on pi
        # self.screen.show()

        # TODO uncomment for actual display
        self.epd.display(self.epd.getbuffer(self.screen))
        time.sleep(2)
        self.epd.sleep()

    def add_event(self, event):
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


def main():
    '''Demo main function to show default displays'''
    screen_controller = Draw()
    screen_controller.show_calendar()
    screen_controller.display()


if __name__ == '__main__':
    main()
