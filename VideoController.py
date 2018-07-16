import threading
import cv2
import imutils


class VideoController(threading.Thread):

    def __init__(self, filename, width=600, rotation=0):
        self._stop_event = threading.Event()
        self.cancelled = False
        threading.Thread.__init__(self)

        self.width = width
        self.rotation = rotation

        self.capture = cv2.VideoCapture(filename)

        self.image = None

    def run(self):
        while not self.is_stopped():
            while self.capture.isOpened():
                ret, new_frame = self.capture.read()
                new_frame = imutils.resize(new_frame, 600)
                self.image = imutils.rotate_bound(new_frame, self.rotation)
            self.stop()

    def stop(self):
        self._stop_event.set()
        self.capture.release()

    def is_stopped(self):
        return self._stop_event.is_set()

    def get_image(self):
        return self.image