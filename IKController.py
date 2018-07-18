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
        self.setup_model()

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


        """
        head_matrix = geometry_utils.to_transformation_matrix(np.array([head_x, 0, head_z]))
        l_wrist_matrix = geometry_utils.to_transformation_matrix(np.array([l_wrist_x, 0, l_wrist_z]))
        r_wrist_matrix = geometry_utils.to_transformation_matrix(np.array([r_wrist_x, 0, r_wrist_z]))
        l_ankle_matrix = geometry_utils.to_transformation_matrix(np.array([l_ankle_x, 0, l_ankle_z]))
        r_ankle_matrix = geometry_utils.to_transformation_matrix(np.array([r_ankle_x, 0, r_ankle_z]))

        print("L arm")
        print(self.left_arm_chain.inverse_kinematics(l_wrist_matrix))
        print(l_wrist_matrix)

        print("R arm")
        print(self.right_arm_chain.inverse_kinematics(r_wrist_matrix))

        print("Head")
        print(self.head_chain.inverse_kinematics(head_matrix))

        print("L ankle")
        print(self.left_leg_chain.inverse_kinematics(l_ankle_matrix))

        print("R ankle")
        print(self.right_leg_chain.inverse_kinematics(r_ankle_matrix))
        """
        angle = math.atan(l_wrist_x / l_wrist_z)
        print(math.degrees(angle))

    # Set up head to chest image distance
    def set_head_to_chest(self, distance):
        self.head_to_chest_distance = distance

    # Set up IK chains
    def setup_model(self):
        self.left_arm_chain = Chain(name='left_arm', links=[
            OriginLink(),
            URDFLink(
              name="shoulder",
              translation_vector=[-0.59, 0, 0.44],
              orientation=[0, 0, 0],
              rotation=[0, 0, 0],
            ),
            URDFLink(
              name="elbow",
              translation_vector=[0, 0, -0.53],
              orientation=[0, 0, 0],
              rotation=[0, 0, 0],
            ),
            URDFLink(
                name="wrist",
                translation_vector=[0, 0, -0.74],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            )],active_links_mask=[False, True, True, True])

        self.right_arm_chain = Chain(name='right_arm', links=[
            OriginLink(),
            URDFLink(
                name="shoulder",
                translation_vector=[0.59, 0, 0.44],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="elbow",
                translation_vector=[0, 0, -0.53],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="wrist",
                translation_vector=[0, 0, -0.74],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            )],active_links_mask=[False, True, True, True])

        self.head_chain = Chain(name='head', links=[
            OriginLink(),
            URDFLink(
                name="neck",
                translation_vector=[0, 0, 1],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="face",
                translation_vector=[0, -0.2, 0],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            )], active_links_mask=[False, True, True])

        self.left_leg_chain = Chain(name='left_leg', links=[
            OriginLink(),
            URDFLink(
                name="hip",
                translation_vector=[0.26, 0, -1.07],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="knee",
                translation_vector=[0, 0, -0.98],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="ankle",
                translation_vector=[0, 0, -1.13],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            )],active_links_mask=[False, True, True, True])

        self.right_leg_chain = Chain(name='right_leg', links=[
            OriginLink(),
            URDFLink(
                name="hip",
                translation_vector=[-0.26, 0, -1.07],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="knee",
                translation_vector=[0, 0, -0.98],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            ),
            URDFLink(
                name="ankle",
                translation_vector=[0, 0, -1.13],
                orientation=[0, 0, 0],
                rotation=[0, 0, 0],
            )],active_links_mask=[False, True, True, True])


