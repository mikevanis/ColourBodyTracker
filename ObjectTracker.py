import cv2
import math
import numpy as np
from imutils import contours as contour_util

class ObjectTracker:

    # Constructor
    def __init__(self, max_distance=60, last_seen_max=30):
        self.max_distance = max_distance
        self.previous = list()
        self.labels = ["chest", "head", "l_wrist", "l_ankle", "r_wrist", "r_ankle"]
        self.last_seen_max = last_seen_max
        pass

    def track(self, contours):
        all_matches = list()
        objects = list()

        # Convert contours to TrackedObject list
        for c in contours:
            objects.append(TrackedObject(c, "unknown"))

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

        # Match objects
        matched_objects = [False] * objects.__len__()
        matched_previous = [False] * self.previous.__len__()
        for match in all_matches:
            i = match.i
            j = match.j

            # If both objects are not matched, then match them.
            if matched_objects[i] is False and matched_previous[j] is False:
                matched_objects[i] = True
                matched_previous[j] = True
                objects[match.i].label = self.previous[match.j].label
                objects[match.i].last_seen = 0

        # Look for missing labels
        for label in self.labels:
            found_object = next((o for o in objects if o.label == label), None)
            if found_object is None:
                # Object not found. Get object from previous and insert to objects list.
                old_object = next((o for o in self.previous if o.label == label), None)
                if old_object is not None:
                    if old_object.last_seen < self.last_seen_max:
                        # Old object is still alive.
                        old_object.last_seen = old_object.last_seen + 1
                        objects.append(old_object)
                    """
                    else:
                        # Old object is dead. Replace with new unmatched.
                        for index, o in enumerate(objects):
                            if o.label == "unknown":
                                objects[index] = old_object
                                break
                    """

        # Find missing legs and hands
        known_labels = list()
        unknown_contours = list()
        for i, o in enumerate(objects):
            if o.label == "unknown":
                unknown_contours.append(o.contour)
                del objects[i]
            else:
                known_labels.append(o.label)

        if unknown_contours.__len__() > 0:
            print("Contours missing.")
            print(unknown_contours.__len__())
            # One limb missing. Easy.
            if unknown_contours.__len__() == 1:
                for l in self.labels:
                    if l not in known_labels:
                        objects.append(TrackedObject(unknown_contours[0], l))

            """
            elif unknown_contours.__len__() == 2:
                # If hands missing:
                if "l_wrist" not in known_labels and "r_wrist" not in known_labels:
                    unknown_contours = contour_util.sort_contours(unknown_contours, method="left-to-right")
                    objects.append(TrackedObject(unknown_contours[0], "l_wrist"))
                    objects.append(TrackedObject(unknown_contours[1], "r_wrist"))
                elif "l_ankle" not in known_labels and "r_ankle" not in known_labels:
                    unknown_contours = contour_util.sort_contours(unknown_contours, method="left-to-right")
                    objects.append(TrackedObject(unknown_contours[0], "l_ankle"))
                    objects.append(TrackedObject(unknown_contours[1], "r_ankle"))
                elif "l_wrist" not in known_labels and "l_ankle" not in known_labels:
                    unknown_contours = contour_util.sort_contours(unknown_contours, method="top-to-bottom")
                    objects.append(TrackedObject(unknown_contours[0], "l_wrist"))
                    objects.append(TrackedObject(unknown_contours[1], "l_ankle"))
                elif "l_wrist" not in known_labels and "r_ankle" not in known_labels:
                    unknown_contours = contour_util.sort_contours(unknown_contours, method="top-to-bottom")
                    objects.append(TrackedObject(unknown_contours[0], "l_wrist"))
                    objects.append(TrackedObject(unknown_contours[1], "r_ankle"))
                elif "r_wrist" not in known_labels and "l_ankle" not in known_labels:
                    unknown_contours = contour_util.sort_contours(unknown_contours, method="top-to-bottom")
                    objects.append(TrackedObject(unknown_contours[0], "r_wrist"))
                    objects.append(TrackedObject(unknown_contours[1], "l_ankle"))
                elif "r_wrist" not in known_labels and "r_ankle" not in known_labels:
                    unknown_contours = contour_util.sort_contours(unknown_contours, method="top-to-bottom")
                    objects.append(TrackedObject(unknown_contours[0], "r_wrist"))
                    objects.append(TrackedObject(unknown_contours[1], "r_ankle"))
            else:
                return None
            """


        # Return found TrackedObjects
        self.previous = objects
        return objects

    # Setup tracking of individual object.
    def track_object(self, contour, label):
        self.previous.append(TrackedObject(contour, label))

    # Setup tracking with list of objects.
    def insert_tracked_objects(self, o_list):
        self.previous = o_list

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

    @staticmethod
    def convert_list_to_dictionary(list_of_objects):
        dictionary = {}
        for item in list_of_objects:
            dictionary[item.label] = item.get_center()
        return dictionary

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

    # Calculate angle between two points
    def calculate_angle(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        angle = math.atan2(b_y - a_y, b_x - a_x)
        angle = math.degrees(angle)
        return angle

    # Map int range
    @staticmethod
    def map_int(x, in_min, in_max, out_min, out_max):
        output = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if output > out_max:
            output = out_max
        if output < out_min:
            output = out_min

        return output


class MatchedPair:

    def __init__(self, i, j, distance):
        self.i = i
        self.j = j
        self.distance = distance


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