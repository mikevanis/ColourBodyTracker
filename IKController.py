from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import ikpy.geometry_utils as geometry_utils
import numpy as np
import math

class IKController:

    # Constructor
    def __init__(self, image_height=600, image_width=400, plot_results=False):
        self.image_height = image_height
        self.image_width = image_width
        self.plot_results = plot_results
        self.head_chain = None
        self.left_arm_chain = None
        self.right_arm_chain = None
        self.left_leg_chain = None
        self.right_leg_chain = None
        self.head_to_chest_distance = 200

    # Compute inverse kinematics from points
    def compute(self, point_dictionary):
        transformed_points = {}

        # Translate and scale points
        chest_x, chest_y = point_dictionary["chest"]
        for label, center in point_dictionary.items():
            x, y = center
            x = (x - chest_x) / self.head_to_chest_distance
            y = (chest_y - y) / self.head_to_chest_distance
            #print("Label: " + label + "\tX: {0:8.2f}\tY: {1:8.2f}".format(x, y))
            transformed_points[label] = (x, y)

        # Extract transformed x y coordinates and structure them as transformation matrices
        head_x, head_z = transformed_points["head"]
        l_wrist_x, l_wrist_z = transformed_points["l_wrist"]
        r_wrist_x, r_wrist_z = transformed_points["r_wrist"]
        l_ankle_x, l_ankle_z = transformed_points["l_ankle"]
        r_ankle_x, r_ankle_z = transformed_points["r_ankle"]

        l_wrist_angle = self.calculate_angle(l_wrist_x, l_wrist_z, chest_x, chest_y)
        print(l_wrist_angle)

    # Set up head to chest image distance
    def set_head_to_chest(self, distance):
        self.head_to_chest_distance = distance

    # Calculate angle between two points
    def calculate_angle(self, a_x, a_y, b_x, b_y):
        angle = math.atan2(b_y - a_y, b_x - a_x)
        angle = math.degrees(angle)
        return angle

    # Map int range
    @staticmethod
    def map_int(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


