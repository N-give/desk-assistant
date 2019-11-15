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
# from lib.waveshare_epd import epd7in5

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

img = Image.new('1', (WIDTH, HEIGHT), 255)  # 255 -> set image to all white
# img = Image.new('1', (epd.width, epd.height), 0)
# 255 -> set image to all white
# 0   -> set image to all black

draw = ImageDraw.Draw(img)

today = datetime.date.today()
draw.text((20, 5), WEEKDAYS[today.weekday()], font=font18, fill=0)
draw.ellipse([(20, 24), (53, 57)], fill=0, outline=0)
draw.text((21.5, 28.5), f'{today.day}', font=font24, fill=255)

# TODO comment out when running on pi
img.show()

# TODO uncomment for actual display
# epd.display(epd.getbuffer(img))
# time.sleep(2)
# epd.Clear()
# time.sleep(2)
# epd.sleep()

class Draw:
    '''Draw class to simplify displaying calendar information'''
    def __init__(self):
        self.screen = Image.new('1', (WIDTH, HEIGHT), 255)
        self.font18 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMonoBold.otf", 18)
        self.draw_screen = ImageDraw.Draw(self.screen)
        self.draw_screen.text((20, 5), WEEKDAYS[today.weekday()], font=font18,
                              fill=0)

        self.draw_screen.ellipse([(20, 24), (53, 57)], fill=0,
                                 outline=0)

        self.draw_screen.text((21.5, 28.5), f'{today.day}', font=font24,
                              fill=255)

    def display(self):
        '''Send image to display'''
        # TODO comment out when running on pi
        self.screen.show()

        # TODO uncomment for actual display
        # epd.display(epd.getbuffer(img))
        # time.sleep(2)
        # epd.Clear()
        # time.sleep(2)
        # epd.sleep()

    def add_event(self, event):
        '''Add event to calendar
        event: to be added to screen
        '''
        # TODO figure out how events will be structured


def main():
    screen_controller = Draw()
    screen_controller.


if __name__ == '__main__':
    main()
