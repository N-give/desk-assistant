'''Draw class implementation for e-paper desk assisstant'''
# import os
import time
import pprint
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont  # type: ignore
from .waveshare_epd import epd7in5

# XXX Set to desired system font or font from ./pic/
# Recommended to use monospace font to ensure alignment shape and text
# alignment
# FreeMonoBold18: 11x18 pixels per char
# FreeMonoBold24: 15x24 pixels per char

# WIDTH = 640
# HEIGHT = 384

pp = pprint.PrettyPrinter(indent=4)

WIDTH = 384
HEIGHT = 640

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

    def __init__(self):
        self.epd = epd7in5.EPD()
        self.epd.init()
        self.epd.Clear()

        # 255 -> set image to all white
        # 0   -> set image to all black
        self.screen = Image.new('1', (WIDTH, HEIGHT), 255)
        self.font18 = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", 18)
        # "/usr/share/fonts/opentype/freefont/FreeMonoBold.otf", 18)
        self.font24 = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", 24)
        # "/usr/share/fonts/opentype/freefont/FreeMonoBold.otf", 24)
        self.draw_screen = ImageDraw.Draw(self.screen)
        # event: title, time, location, privacy
        self.events = [{
            'title': 'ECE 40862 Demo',
            'start_weekday': 'Thursday',
            'start_date': '2019-11-20',
            'start_time': '14:30:00',
            'end_weekday': 'Thursday',
            'end_date': '2019-11-20',
            'end_time': '15:00:00',
            'location': None,
            'privacy': 'public'
        }]
        self.days = {}
        self.times = {}

    # def __del__(self):
    #     # self.epd.Clear()
    #     epd7in5.epdconfig.module_exit()

    def clear_screen(self):
        '''Get fresh image so the screen can be redrawn'''
        self.screen = Image.new('1', (WIDTH, HEIGHT), 255)
        self.draw_screen = ImageDraw.Draw(self.screen)

    def show_away(self):
        '''Setup display to show away screen'''
        self.epd.Clear()
        self.clear_screen()
        self.draw_screen.text((WIDTH / 2, HEIGHT / 2), "LOCKED",
                              fill=0, font=self.font24)

    def show_calendar(self):
        '''Setup display to show calendar'''
        self._draw_grid()
        self._draw_events()

    def _draw_events(self):
        # TODO create generator over event to check public setting
        for event in self.events:
            start_event = datetime.strptime(
                "{} {}".format(event['start_date'], event['start_time']),
                "%Y-%m-%d %H:%M:%S")
            end_event = datetime.strptime(
                "{} {}".format(event['end_date'], event['end_time']),
                "%Y-%m-%d %H:%M:%S")

            # TODO these need to be found to the nearest half hour then
            # adjusted when they're in between because only the lines drawn
            # on half hour intervals

            # TODO only +/- 2 pixels from top/bottom when time falls on time
            # line boundary

            # TODO add case when an event beginning has already already passed
            # but the event hasn't ended yet
            
            edges = self._get_event_edges(start_event, end_event)
            print(edges)
            if all(edges):
                etop, eleft, eright, ebottom = edges

                # draw side lines with space to create rounded corners
                # top
                self.draw_screen.line(
                    [((eleft + RADIUS), etop), ((eright - RADIUS), etop)],
                    fill=0, width=1)
                # bottom
                self.draw_screen.line(
                    [((eleft + RADIUS), ebottom),
                     ((eright - RADIUS), ebottom)],
                    fill=0, width=1)
                # left
                self.draw_screen.line(
                    [(eleft, (etop + RADIUS)),
                     (eleft, (ebottom - RADIUS))],
                    fill=0, width=1)
                # right
                self.draw_screen.line(
                    [(eright, (etop + RADIUS)),
                     (eright, (ebottom - RADIUS))],
                    fill=0, width=1)

                # draw arcs to connect event sides
                # top left corner
                self.draw_screen.arc(
                    [(eleft, etop),
                     ((eleft + (2*RADIUS)), (etop + (2*RADIUS)))],
                    180, 270, fill=0, width=1)
                # top right corner
                self.draw_screen.arc(
                    [((eright - (2*RADIUS)), etop),
                     (eright, (etop + (2*RADIUS)))],
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

                self.draw_screen.text(((eleft + 2), (etop + 2)),
                                      event['title'],
                                      font=self.font18, fill=0)

            else:
                print('Event not currently displayed on calendar.')
                pp.pprint(event)

    def _draw_grid(self):
        today = datetime.today()

        # setup time grid for day
        # Get width for 3 days to be displayed
        date_line = 65
        grid_width = (WIDTH - 10) - date_line
        day_width = grid_width

        # Get spacing to display 5 time lines
        time_line = 60
        grid_height = (HEIGHT - 10) - time_line
        time_height = grid_height / 7

        # Draw lines for each day displayed
        for i in range(1):
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
                                  '{:2}'.format(today.day + i),
                                  font=self.font24, fill=255)
            date_line += day_width

        # Draw last line to close calendar grid
        self.days[today.day + 1] = date_line
        self.draw_screen.line([(date_line, 60),
                               (date_line, (HEIGHT - 10))], fill=0)

        # Draw time lines
        current_hour, current_minute = _get_closest_time(today)
        while time_line < HEIGHT:
            self.times[(current_hour, current_minute)] = time_line
            self.draw_screen.line([(60, time_line),
                                   ((WIDTH - 10), time_line)], fill=0)
            self.draw_screen.text((6, (time_line - 9)),
                                  '{:02}:{:02}'.format(
                                      (current_hour % 24), current_minute),
                                  fill=0, font=self.font18)
            current_minute += 30
            if current_minute == 60:
                current_minute = 0
                current_hour += 1

            time_line += time_height

    def _get_event_edges(self, start, end):
        top = None
        left = None  # self.days[start.day]
        right = None  # self.days[start.day + 1]
        bottom = None

        try:
            top = self.times[_get_closest_time(start)]
        except KeyError:
            top = None

        try:
            left = self.days[start.day] + 2
        except KeyError:
            left = None

        try:
            right = self.days[start.day + 1] - 2
        except KeyError:
            right = None

        try:
            bottom = self.times[_get_closest_time(end)]
        except KeyError:
            bottom = None

        return (top, left, right, bottom)

    def display(self):
        '''Send image to display'''
        # TODO comment out when running on pi
        # self.screen.show()

        # TODO uncomment for actual display
        self.epd.display(self.epd.getbuffer(self.screen))
        time.sleep(2)
        # self.epd.sleep()

    def add_events(self, events):
        '''
        Add event to calendar
        events: list of events to be added to display
            - title: Title of event to be displayed on calendar
            - start_weekday: Weekday on which event begins
            - start_date: Date on which event begins
                `yyyy-mm-dd`
            - start_time: Time at which event begins
                `hh:mm:ss`
            - end_weekday: Weekday on which event ends
            - end_date: Date on which event ends
            - end_time: Time at which event ends
            - location: Location of event if provided
            - privacy: Privacy of event
                - Controlls whether event should be displayed while user is
                  away from desk or not

        Example event:
            {
                'title': '40862 Exam',
                'start_weekday': 'Thursday',
                'start_date': '2019-11-21',
                'start_time': '12:00:00',
                'end_weekday': 'Thursday',
                'end_date': '2019-11-21',
                'end_time': '13:15:00',
                'location': None,
                'privacy': 'public'
            }
        '''
        self.events = events


def _get_closest_time(time_stamp):
    '''Get initial time set to most recent 30 minute mark'''
    # closest_interval: int = (time_stamp.minute // 10) * 10
    if time_stamp.minute >= 30:
        closest_interval = 30
    else:
        closest_interval = 0

    return (time_stamp.hour, closest_interval)


def main():
    '''Demo main function to show default displays'''
    screen_controller = Draw()
    screen_controller.show_calendar()
    screen_controller.display()


if __name__ == '__main__':
    main()
