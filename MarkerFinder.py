import cv2
import numpy as np

class MarkerFinder:

    # Constructor
    def __init__(self, min_radius=10, show_mask="False"):
        self.min_radius = min_radius
        self.show_mask = show_mask
        pass

    # Find markers and return point list
    def find(self, image):
        points = list()

        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        #blurred = (255 - blurred)
        frame_to_thresh = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        #blue_lower = np.array([100, 150, 20], np.uint8)
        #blue_upper = np.array([140, 255, 255], np.uint8)
        #thresh = cv2.inRange(frame_to_thresh, blue_lower, blue_upper)
        #lower_cyan = (90 - 10, 70, 50)
        #upper_cyan = (90 + 10, 255, 255)
        #thresh = cv2.inRange(frame_to_thresh, lower_cyan, upper_cyan)
        lower_red = (170, 150, 50)
        upper_red = (180, 255, 255)

        thresh = cv2.inRange(frame_to_thresh, lower_red, upper_red)

        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            moment = cv2.moments(c)
            center = (int(moment["m10"] / moment["m00"]), int(moment["m01"] / moment["m00"]))

            if radius > self.min_radius:
                print(radius)
                points.append(center)

        if self.show_mask is True:
            thresh_output = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            output = np.hstack((thresh_output, blurred))
            cv2.imshow("Colour Tracking", output)

        return points
