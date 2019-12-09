'''
E-Paper Calendar Desk Assistant with Google Calendar Integration
'''

# from typing import List

from lib.draw_screen import Draw
from lib.g_calender_api import G_calendar  # type: ignore
from facial_recognition_class import face_detection
import signal
from signal import alarm, signal, SIGALRM
import select
import sys
import time
import requests

def main():
    face = False
    clear = True
    '''
    E-Paper Calendra Desk Assistant with Google Calendar Integration
    - Ensure token.pickle and credentials.json are in project root directory
    '''
    camera = face_detection()
    
##    def getInput():
##        temp = input("Press enter to unlock ")
##        return temp
   
    calendar = G_calendar()
    screen = Draw()
    screen.show_away()
    screen.display()
    while(True):
##        if x == 'y':
##            face = camera.recognize_faces()
##        elif x == 'l':
##            face = False
##            print("You are done")
##            time.sleep(5)
##            
##        if face:
##            print("Updated")
        if face == True:
            print("first")
            if camera.recognize_faces():
                screen.clear_screen() #  = Draw() ##crashes
                calendar.update_events()
                
                events = calendar.get_events()
                screen.add_events(events)
                screen.show_calendar()
                screen.display()
                face = True
                clear = False
                time.sleep(5)
            else:
                print("hi")
                r = requests.post("https://maker.ifttt.com/trigger/update_log/with/key/pSaBhwacOFzl-hJpYXwmwOCI0RStK8DkuIQrVx8rqcx", params={"value1":"logged out"})
                face = False
                time.sleep(5)

        elif camera.recognize_faces():
            r = requests.post("https://maker.ifttt.com/trigger/update_log/with/key/pSaBhwacOFzl-hJpYXwmwOCI0RStK8DkuIQrVx8rqcx", params={"value1":"logged in"})
            screen.clear_screen() # = Draw()    
            calendar.update_events()
            events = calendar.get_events()
            screen.add_events(events)
            screen.show_calendar()
            screen.display()
            face = True
            clear = False
            time.sleep(5)
        else:
            if clear == False:
                print("locked")
                screen.show_away()
                screen.display()
                face = False
                clear = True
                time.sleep(5)
            else:
                print("sup")
                time.sleep(5)

            
 

if __name__ == '__main__':
    main()
