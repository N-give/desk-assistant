'''Draw functions required for e-paper desk assisstant'''

# import sys
# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#         sys.path.append(libdir)
# 

import os
import time
from lib.waveshare_epd import epd7in5
from PIL import Image,ImageDraw,ImageFont

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

epd = epd7in5.EPD()
epd.init()
epd.Clear()

img = Image.new('1', (epd.width, epd.height), 0) # 255 -> set image to all white
                                                   # 0   -> set image to all black
draw = ImageDraw.Draw(img)
draw.text((20, 5), "Test placement", font=font24, fill=255)

epd.display(epd.getbuffer(img))
time.sleep(2)
epd.Clear()
time.sleep(2)
epd.sleep()
