import cv2
import numpy as np

class MarkerFinder:

    # Constructor
    def __init__(self, min_radius=10, show_mask="False"):
        self.min_radius = min_radius
        self.show_mask = show_mask
        pass

    # Find contours
    def find_contours(self, image):
        contours = list()

        # Blur, convert to HSV, threshold, erode, dilate.
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        frame_to_thresh = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        lower_red = (170, 110, 50)
        upper_red = (180, 255, 255)
        thresh = cv2.inRange(frame_to_thresh, lower_red, upper_red)
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Eliminate small contours
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > self.min_radius:
                contours.append(c)
                pass

        # Show mask
        if self.show_mask is True:
            thresh_output = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            output = np.hstack((thresh_output, blurred))
            cv2.imshow("Colour Tracking", output)

        return contours


