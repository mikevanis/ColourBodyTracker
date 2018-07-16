import cv2
import math
import numpy as np
from imutils import contours as contour_util

class ObjectTracker:

    # Constructor
    def __init__(self, max_distance=20):
        self.max_distance = max_distance
        self.previous = list()
        self.current = list()
        pass

    def track(self, objects):
        all_matches = list()

        # Iterate through both
        for (i, n_object) in enumerate(objects):
            n_x, n_y = n_object.get_center()
            for (j, m_object) in enumerate(self.previous):
                m_x, m_y = m_object.get_center()

                # Calculate distance
                distance = self.calculate_distance(n_x, n_y, m_x, m_y)
                if distance < self.max_distance:
                    # Possible match - add MatchedPair to list of matches.
                    all_matches.append(MatchedPair(i, j, distance))

        # Sort all matches - closest first
        all_matches.sort(key=lambda x: x.distance)

        results = list()

        # Loop through first six matches with shortest distances
        for match in all_matches[:6]:
            # Change labels
            objects[match.i].label = self.previous[match.j].label
            results.append(objects[match.i])

        # Return found TrackedObjects
        return results

    # Setup tracking of individual object.
    def track_object(self, contour, label):
        self.previous.append(TrackedObject(contour, label))

    # Sort contours
    def label_contours(self, contours):
        if not contours:
            return None

        elif contours.__len__() == 6:
            results = list()

            # Find largest contour, the chest.
            largest_contour, largest_contour_index = self.get_largest_contour(contours)
            del contours[largest_contour_index]
            results.append(TrackedObject(largest_contour, "chest"))

            # Sort contours top to bottom, left to right.
            left_to_right_contours, _ = contour_util.sort_contours(contours, method="left-to-right")
            top_to_bottom_contours, _ = contour_util.sort_contours(contours, method="top-to-bottom")

            # Find head - first one from the top.

            matches = list()

            for (t, ttb_contour) in enumerate(top_to_bottom_contours):
                ttb_area = cv2.contourArea(ttb_contour)
                for (l, ltr_contour) in enumerate(left_to_right_contours):
                    ltr_area = cv2.contourArea(ltr_contour)

                    if ttb_area == ltr_area:
                        matches.append(MatchedPair(t, l, 0))

            for match in matches:
                # Head
                if match.i == 0:
                    results.append(TrackedObject(top_to_bottom_contours[0], "head"))

                # Left side
                if match.j == 0 or match.j == 1:
                    if match.i == 1 or match.i == 2:
                        # Left wrist
                        results.append(TrackedObject(top_to_bottom_contours[match.i], "l_wrist"))
                    elif match.i == 3 or match.i == 4:
                        # Left ankle
                        results.append(TrackedObject(top_to_bottom_contours[match.i], "l_ankle"))

                # Right side
                elif match.j == 3 or match.j == 4:
                    if match.i == 1 or match.i == 2:
                        # Right wrist
                        results.append(TrackedObject(top_to_bottom_contours[match.i], "r_wrist"))
                    elif match.i == 3 or match.i == 4:
                        # Right ankle
                        results.append(TrackedObject(top_to_bottom_contours[match.i], "r_ankle"))

            return results

    # Calculate distance between two points
    @staticmethod
    def calculate_distance(a_x, a_y, b_x, b_y):
        return math.sqrt((b_x - a_x) ** 2 + (b_y - a_y) ** 2)

    @staticmethod
    def get_largest_contour(contours):
        if not contours:
            return None
        else:
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            return contours[max_index], max_index


class MatchedPair:

    def __init__(self, i, j, dist):
        self.i = i
        self.j = j
        self.dist = dist


class TrackedObject:

    # Constructor
    def __init__(self, contour, label):
        self.contour = contour
        self.last_seen = 0
        self.age = 0
        self.label = label

    def time_step(self, visible):
        self.age = self.age + 1
        if visible is False:
            self.last_seen = self.last_seen + 1

    # Get the object's center x y coordinates
    def get_center(self):
        M = cv2.moments(self.contour)
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        return x, y