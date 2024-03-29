from imutils import paths
import numpy as np
import imutils
import pickle
import cv2
import os
import shutil

# packages needed for encoding the faces
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# packages needed for detection
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2


class face_detection:

    def __init__(self, dataset="dataset", encodings="encodings.pickle", detection_method="hog", cascade="haarcascade_frontalface_default.xml"):
        self.args = locals()
        print(self.args)

        # INITIALIZE CAMERA
        self.dataset_num_frames = 10  # Number of frames to capture for a dataset
        self.detection_num_frames = 40  # Number of frames to capture when trying to unlock
        self.detection_num_success_frames = 5  # Number of frames where the user is detected to unlock
        self.user_name = "Anthony"

    def clear_dataset(self):
        users = os.listdir("dataset")
        for user in users:
            if user is not "unknown":
                shutil.rmtree(os.path.join("dataset", user))


    def encode_faces(self):
        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(self.args["dataset"]))

        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb,
                model=self.args["detection_method"])

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(self.args["encodings"], "wb")
        f.write(pickle.dumps(data))
        f.close()

    def recognize_faces(self):
        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        print("[INFO] loading encodings + face detector...")
        data = pickle.loads(open(self.args["encodings"], "rb").read())
        detector = cv2.CascadeClassifier(self.args["cascade"])

        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

        # start the FPS counter
        fps = FPS().start()

        frames_found = 0
        # loop over frames from the video file stream
        for frame_num in range(1, self.detection_num_frames+1):
            print(frame_num)
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            frame = vs.read()
            frame = imutils.resize(frame, width=500)

            # convert the input frame from (1) BGR to grayscale (for face
            # detection) and (2) from BGR to RGB (for face recognition)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # detect faces in the grayscale frame
            rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

            # OpenCV returns bounding box coordinates in (x, y, w, h) order
            # but we need them in (top, right, bottom, left) order, so we
            # need to do a bit of reordering
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []


            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)

            if self.user_name in names:
                frames_found = frames_found + 1
                print("\tfound")

            if frames_found == self.detection_num_success_frames:
                # stop the timer and display FPS information
                fps.stop()
                print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
                print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
                print("[INFO] Unlock Success: found {} in {} frames within {} samples".format(self.user_name, self.detection_num_success_frames, frame_num))
                # do a bit of cleanup
                cv2.destroyAllWindows()
                vs.stop()
                return True


            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top), (right, bottom),
                              (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)

            # display the image to our screen
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(50) & 0xFF

            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        print("[INFO] Unlock Failed: found {} in {} frames in {} samples".format(self.user_name,
                                                                                      frames_found,
                                                                                      frame_num))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

        return False


if __name__ == "__main__":
    a = face_detection()
    #a.encode_faces()
    print(a.recognize_faces())
    #a.clear_dataset()
    #a.locate_user()
