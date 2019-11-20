'''
E-Paper Calendar Desk Assistant with Google Calendar Integration
'''

# from typing import List

from lib.draw_screen import Draw
from lib.g_calender_api import G_calendar  # type: ignore


def main():
    '''
    E-Paper Calendra Desk Assistant with Google Calendar Integration
    - Ensure token.pickle and credentials.json are in project root directory
    '''

    calendar = G_calendar()
    screen = Draw()

    events = calendar.get_events()
    screen.add_events(events)
    screen.show_calendar()
    screen.display()
    # print(events)


if __name__ == '__main__':
    main()
