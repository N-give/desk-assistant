from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import calendar

# TODO: What data type does screen driver need to writ fonts?
#       What exactly are we going to display interms of events?
#       Make event table
#

# NOTE: May need to run
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def _get_weekday(date):
    '''Return the day of the week for the date'''
    date = datetime.datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[date])


class G_calendar:

    # If modifying these scopes, delete the file token.pickle.

    def __init__(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        self.events_handler = service
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        #print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        self.events = events_result.get('items', [])

    def update_events(self):
        '''Update event list'''

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.events_handler.events().list(calendarId='primary', timeMin=now,
                                                          maxResults=10, singleEvents=True,
                                                          orderBy='startTime').execute()
        self.events = events_result.get('items', [])

    def print_events(self):
        ''' Print event list '''
        events = self.events
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def _get_weekday(date):
        '''Return the day of the week for the date'''
        date = datetime.datetime.strptime(date, '%d %m %Y').weekday()
        return (calendar.day_name[date])

    def get_events(self):
        ''' Return a neat list of the coming events '''
        event_list = []
        events = self.events
        if not events:
            print('No upcoming events found.')
        for event in events:
            event_dict = {}
            event_dict['title'] = event['summary']

            date_list = event['start'].get(
                'dateTime', event['start'].get('date')).split('-')  # yyyy-mm-dd
            event_dict['weekday'] = _get_weekday(
                date_list[2][:2]+" "+date_list[1]+" "+date_list[0])  # dd mm yyyy

            if event['start'].get('dateTime') is not None:
                time_list = event['start'].get('dateTime').split('T')
                event_dict['date'] = time_list[0]
                event_dict['time'] = time_list[1].split('-')[0]
            else:
                event_dict['date'] = event['start'].get('date')
                event_dict['time'] = None

            event_dict['location'] = event.get('location')
            event_dict['privacy'] = 'public'
            print(event_dict)
            event_list.append(event_dict)
        # print(event_list)
        # [{'title': 'ECE 40862 Exam', 'weekday': 'Thursday', 'date': '2019-11-21', 'time': '12:00:00', 'location': 'Math 175', 'privacy': 'public'}]
        return event_list


def main():

    handle = G_calendar()
    handle.update_events()
    handle.print_events()
    handle.get_events()


# init event list
# update event list
# get event list
# print event list


if __name__ == '__main__':
    main()
