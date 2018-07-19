import cv2
import imutils
import sys
import argparse
from imutils.video import FileVideoStream
import time
sys.path.insert(0, 'CameraController')
from CameraController import CameraController
from VideoController import VideoController
from MarkerFinder import MarkerFinder
from ObjectTracker import ObjectTracker
from IKController import IKController
from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--test_video")
args = parser.parse_args()

marker_finder = MarkerFinder(show_mask=True, min_radius=4)
object_tracker = ObjectTracker()
ik_controller = None

has_found_limbs = False

if __name__ == '__main__':
    client = udp_client.SimpleUDPClient("localhost", 8000)

    if args.test_video is None:
        cam = CameraController(width=600, height=400)
        cam.start()

        try:
            while True:
                current_frame = cam.get_image()

                if current_frame is not None:
                    current_frame = imutils.resize(current_frame, 600)
                    current_frame = imutils.rotate_bound(current_frame, 270)
                    contours = marker_finder.find_contours(current_frame)
                    if has_found_limbs is True:
                        tracked_objects = object_tracker.track(contours)
                        point_dictionary = {}

                        organised_limbs = object_tracker.convert_list_to_dictionary(tracked_objects)

                        try:
                            head_angle = object_tracker.calculate_angle(organised_limbs["head"], organised_limbs["chest"])
                            head_mapped = object_tracker.map_int(head_angle, 86, 100, -0.3, 0.3)
                            head_2_mapped = head_mapped*-1
                            client.send_message("/head", head_mapped)
                            client.send_message("/head2", head_2_mapped)
                        except KeyError as e:
                            print(e)

                        try:
                            l_wrist_angle = object_tracker.calculate_angle(organised_limbs["l_wrist"], organised_limbs["chest"])
                            l_wrist_mapped = object_tracker.map_int(l_wrist_angle+45, 179, -179, -1, 1)
                            client.send_message("/l_wrist", l_wrist_mapped)
                        except KeyError as e:
                            print(e)

                        try:
                            l_ankle_angle = object_tracker.calculate_angle(organised_limbs["l_ankle"], organised_limbs["chest"])
                            l_ankle_mapped = object_tracker.map_int(l_ankle_angle+90, 179, -179, -1, 1)
                            client.send_message("/l_ankle", l_ankle_mapped)
                        except KeyError as e:
                            print(e)

                        try:
                            r_wrist_angle = object_tracker.calculate_angle(organised_limbs["r_wrist"], organised_limbs["chest"])
                            r_wrist_angle = r_wrist_angle % 360
                            if r_wrist_angle < 0:
                                r_wrist_angle = r_wrist_angle + 360
                            r_wrist_mapped = object_tracker.map_int(r_wrist_angle-45, 0, 360, -1, 1)
                            client.send_message("/r_wrist", r_wrist_mapped)
                        except KeyError as e:
                            print(e)


                        try:
                            r_ankle_angle = object_tracker.calculate_angle(organised_limbs["r_ankle"], organised_limbs["chest"])
                            r_ankle_angle = r_ankle_angle % 360
                            if r_ankle_angle < 0:
                                r_ankle_angle = r_ankle_angle + 360
                            print(r_ankle_angle)
                            r_ankle_mapped = object_tracker.map_int(r_ankle_angle-100, 0, 360, -1, 1)
                            client.send_message("/r_ankle", r_ankle_mapped)
                        except KeyError as e:
                            print(e)

                        for limb in tracked_objects:
                            cv2.putText(current_frame, limb.label, limb.get_center(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                    else:
                        # Look for limbs and insert them into the tracker.
                        found_limbs = object_tracker.label_contours(contours)

                        # Setup ik controller
                        #height, width, channels = current_frame.shape
                        #ik_controller = IKController(image_height=height, image_width=width, plot_results=True)

                        if found_limbs is not None:
                            object_tracker.insert_tracked_objects(found_limbs)
                            chest = next((o for o in found_limbs if o.label == "chest"), None)
                            chest_x, chest_y = chest.get_center()
                            head = next((o for o in found_limbs if o.label == "head"), None)
                            head_x, head_y = head.get_center()
                            #ik_controller.set_head_to_chest(object_tracker.calculate_distance(chest_x, chest_y, head_x, head_y))
                            has_found_limbs = True
                            print("Found limbs")
                    cv2.imshow("Result", current_frame)
                key = cv2.waitKey(1)


                if key == ord('q'):
                    cam.stop()
                    cam.join()
                    cv2.destroyAllWindows()
                    break

        except KeyboardInterrupt:
            cam.stop()
            cam.join()
            cv2.destroyAllWindows()
            pass

    else:
        video = VideoController(args.test_video, rotation=270)
        video.start()

        try:
            while video.is_stopped() is False:
                current_frame = video.get_image()

                if current_frame is not None:
                    contours = marker_finder.find_contours(current_frame)
                    if has_found_limbs is True:
                        tracked_objects = object_tracker.track(contours)
                        point_dictionary = {}

                        organised_limbs = object_tracker.convert_list_to_dictionary(tracked_objects)
                        chest_x, chest_y = organised_limbs["chest"]
                        head_x, head_y = organised_limbs["head"]

                        head_angle = object_tracker.calculate_angle(organised_limbs["head"], organised_limbs["chest"])
                        head_mapped = object_tracker.map_int(head_angle, 86, 100, -0.3, 0.3)
                        head_2_mapped = head_mapped*-1
                        client.send_message("/head", head_mapped)
                        client.send_message("/head2", head_2_mapped)

                        l_wrist_angle = object_tracker.calculate_angle(organised_limbs["l_wrist"], organised_limbs["chest"])
                        l_wrist_mapped = object_tracker.map_int(l_wrist_angle+45, 179, -179, -1, 1)
                        client.send_message("/l_wrist", l_wrist_mapped)

                        l_ankle_angle = object_tracker.calculate_angle(organised_limbs["l_ankle"], organised_limbs["chest"])
                        l_ankle_mapped = object_tracker.map_int(l_ankle_angle+90, 179, -179, -1, 1)
                        client.send_message("/l_ankle", l_ankle_mapped)

                        r_wrist_angle = object_tracker.calculate_angle(organised_limbs["r_wrist"], organised_limbs["chest"])
                        r_wrist_angle = r_wrist_angle % 360
                        if r_wrist_angle < 0:
                            r_wrist_angle = r_wrist_angle + 360
                        r_wrist_mapped = object_tracker.map_int(r_wrist_angle-45, 0, 360, -1, 1)
                        client.send_message("/r_wrist", r_wrist_mapped)

                        r_ankle_angle = object_tracker.calculate_angle(organised_limbs["r_ankle"], organised_limbs["chest"])
                        r_ankle_angle = r_ankle_angle % 360
                        if r_ankle_angle < 0:
                            r_ankle_angle = r_ankle_angle + 360
                        print(r_ankle_angle)
                        r_ankle_mapped = object_tracker.map_int(r_ankle_angle-190, 0, 360, -1, 1)
                        client.send_message("/r_ankle", r_ankle_mapped)

                        for limb in tracked_objects:
                            cv2.putText(current_frame, limb.label, limb.get_center(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                    else:
                        # Look for limbs and insert them into the tracker.
                        found_limbs = object_tracker.label_contours(contours)
                        object_tracker.insert_tracked_objects(found_limbs)

                        # Setup ik controller
                        height, width, channels = current_frame.shape
                        ik_controller = IKController(image_height=height, image_width=width, plot_results=True)

                        if found_limbs is not None:
                            chest = next((o for o in found_limbs if o.label == "chest"), None)
                            chest_x, chest_y = chest.get_center()
                            head = next((o for o in found_limbs if o.label == "head"), None)
                            head_x, head_y = head.get_center()
                            ik_controller.set_head_to_chest(object_tracker.calculate_distance(chest_x, chest_y, head_x, head_y))
                            #has_found_limbs = True

                    #cv2.imshow("Result", current_frame)
                key = cv2.waitKey(1)


                if key == ord('q'):
                    video.stop()
                    video.join()
                    cv2.destroyAllWindows()
                    break

        except KeyboardInterrupt:
            video.stop()
            video.join()
            cv2.destroyAllWindows()
