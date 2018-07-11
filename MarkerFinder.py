import cv2


class MarkerFinder:

    # Constructor
    def __init__(self, min_radius=10):
        self.min_radius = min_radius
        pass

    # Find markers and return point list
    def find(self, image):
        points = list()

        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        blurred = (255 - blurred)
        frame_to_thresh = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        lower_cyan = (85 - 10, 70, 50)
        upper_cyan = (85 + 10, 255, 255)
        thresh = cv2.inRange(frame_to_thresh, lower_cyan, upper_cyan)
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            moment = cv2.moments(c)
            center = (int(moment["m10"] / moment["m00"]), int(moment["m01"] / moment["m00"]))

            if radius > self.min_radius:
                points.append(center)

        return points
