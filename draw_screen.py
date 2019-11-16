'''Draw class implementation for e-paper desk assisstant'''
from typing import Tuple, Dict, List
# import os
# import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont  # type: ignore
# from lib.waveshare_epd import epd7in5 # type: ignore

# XXX Set to desired system font or font from ./pic/
# Recommended to use monospace font to ensure alignment shape and text
# alignment
# FreeMonoBold18: 11x18 pixels per char
# FreeMonoBold24: 15x24 pixels per char

WIDTH = 640
HEIGHT = 384

RADIUS = 10

WEEKDAYS = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun"
}


class Draw:
    '''Draw class to simplify displaying calendar information'''

    def __init__(self) -> None:
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
        # event: title, time, location, privacy
        self.events: List[Dict[str, str]] = [{
            'title': 'event1',
            'time': '2019-11-16 17:00:00',
            'location': '...here',
            'privacy': 'none'
        }]
        self.days: Dict[int, float] = {}
        self.times: Dict[Tuple[int, int], float] = {}

    def show_away(self) -> None:
        '''Setup display to show away screen'''

    def show_calendar(self) -> None:
        '''Setup display to show calendar'''
        today = datetime.today()

        # setup time grid for day
        # Get width for 3 days to be displayed
        date_line: float = 65
        grid_width: float = (WIDTH - 10) - date_line
        day_width: float = grid_width / 3

        # Get spacing to display 5 time lines
        time_line: float = 60
        grid_height: float = (HEIGHT - 10) - time_line
        time_height: float = grid_height / 5

        # Draw lines for each day displayed
        for i in range(3):
            self.days[today.day + i] = date_line
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

        # Draw last line to close calendar grid
        self.draw_screen.line([(date_line, 60),
                               (date_line, (HEIGHT - 10))], fill=0)

        # Draw time lines
        current_hour, current_minute = get_initial_time(today)
        while time_line < HEIGHT:
            self.times[(current_hour, current_minute)] = time_line
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

        for event in self.events:
            event_time = datetime.strptime(
                event['time'], "%Y-%m-%d %H:%M:%S")

            # TODO these need to be found to the nearest half hour then adjusted
            # when they're in between because only the lines drawn on half hour
            # intervals
            # TODO only +/- 2 pixels from top/bottom when time falls on time
            # line boundary
            # TODO add case when an event beginning has already already passed
            # but the event hasn't ended yet
            etop = self.times[(event_time.hour, event_time.minute)] + 2
            eleft = self.days[event_time.day] + 2
            eright = self.days[event_time.day + 1] - 2
            ebottom = self.times[((event_time.hour + 1),
                                  event_time.minute)] - 2

            # draw side lines with space to create rounded corners
            # top
            self.draw_screen.line(
                [((eleft + RADIUS), etop), ((eright - RADIUS), etop)],
                fill=0, width=1)
            # bottom
            self.draw_screen.line(
                [((eleft + RADIUS), ebottom), ((eright - RADIUS), ebottom)],
                fill=0, width=1)
            # left
            self.draw_screen.line(
                [(eleft, (etop + RADIUS)), (eleft, (ebottom - RADIUS))],
                fill=0, width=1)
            # right
            self.draw_screen.line(
                [(eright, (etop + RADIUS)), (eright, (ebottom - RADIUS))],
                fill=0, width=1)

            # draw arcs to connect event sides
            # top left corner
            self.draw_screen.arc(
                [(eleft, etop), ((eleft + (2*RADIUS)), (etop + (2*RADIUS)))],
                180, 270, fill=0, width=1)
            # top right corner
            self.draw_screen.arc(
                [((eright - (2*RADIUS)), etop), (eright, (etop + (2*RADIUS)))],
                270, 0, fill=0, width=1)
            # bottom left corner
            self.draw_screen.arc(
                [(eleft, (ebottom - (2*RADIUS))),
                 ((eleft + (2*RADIUS)), ebottom)],
                90, 180, fill=0, width=1)
            # bottom right corner
            self.draw_screen.arc(
                [((eright - (2*RADIUS)), (ebottom - (2*RADIUS))),
                 (eright, ebottom)],
                0, 90, fill=0, width=1)

    def display(self) -> None:
        '''Send image to display'''
        # TODO comment out when running on pi
        self.screen.show()

        # TODO uncomment for actual display
        # self.epd.display(self.epd.getbuffer(self.screen))
        # time.sleep(2)
        # self.epd.sleep()

    def add_event(self, events: List[Dict[str, str]]) -> None:
        '''Add event to calendar
        event: to be added to screen
        '''
        # TODO figure out how events will be structured
        # event = dict:
        #       title
        #       time
        #       name
        #       location
        #       privacy

        self.events += events


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
