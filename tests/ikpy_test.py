from ikpy.chain import Chain
import ikpy.geometry_utils as geometry_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
from ikpy.link import OriginLink, URDFLink
import numpy as np

left_arm_chain = Chain(name='left_arm', links=[
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

right_arm_chain = Chain(name='right_arm', links=[
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

head_chain = Chain(name='head', links=[
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

left_leg_chain = Chain(name='left_leg', links=[
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

right_leg_chain = Chain(name='right_leg', links=[
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


ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
target_vector = [ 0.1, -0.2, 0.1]
l_wrist_matrix = geometry_utils.to_transformation_matrix(target_vector)
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector

left_arm_start_position = left_arm_chain.forward_kinematics([0] * 4)
right_arm_start_position = right_arm_chain.forward_kinematics([0] * 4)
head_start_position = head_chain.forward_kinematics([0] * 3)
left_leg_start_position = left_leg_chain.forward_kinematics([0] * 4)
right_leg_start_position = right_leg_chain.forward_kinematics([0] * 4)

print(right_arm_start_position)

left_arm_chain.plot(left_arm_chain.inverse_kinematics(l_wrist_matrix), ax, target=target_vector)
right_arm_chain.plot(right_arm_chain.inverse_kinematics(right_arm_start_position), ax)
head_chain.plot(head_chain.inverse_kinematics(head_start_position), ax)
left_leg_chain.plot(left_leg_chain.inverse_kinematics(left_leg_start_position), ax)
right_leg_chain.plot(right_leg_chain.inverse_kinematics(right_leg_start_position), ax)

matplotlib.pyplot.show()