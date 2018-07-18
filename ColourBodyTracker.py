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

parser = argparse.ArgumentParser()
parser.add_argument("--test_video")
args = parser.parse_args()

marker_finder = MarkerFinder(show_mask=False, min_radius=4)
object_tracker = ObjectTracker()
ik_controller = None

has_found_limbs = False

if __name__ == '__main__':
    if args.test_video is None:
        cam = CameraController(width=600, height=400)
        cam.start()

        try:
            while True:
                current_frame = cam.get_image()

                if current_frame is not None:
                    marker_finder.find_contours(current_frame)

                    """
                    for p in points:
                        cv2.circle(current_frame, p, 5, (255, 0, 255), -1)
            
                    cv2.imshow("Result", current_frame)
                    """

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
                        l_wrist_x, l_wrist_y = organised_limbs["l_wrist"]
                        angle = object_tracker.calculate_angle(l_wrist_x, l_wrist_y, chest_x, chest_y)
                        print(angle)

                        for limb in tracked_objects:
                            point_dictionary[limb.label] = limb.get_center()
                            cv2.putText(current_frame, limb.label, limb.get_center(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        #print(object_tracker.calculate_angle(l_wrist_y, chest_y, l_wrist_x, chest_x))
                        #ik_controller.compute(point_dictionary)

                    else:
                        # Look for limbs and insert them into the tracker.
                        found_limbs = object_tracker.label_contours(contours)
                        object_tracker.insert_tracked_objects(found_limbs)

                        # Setup ik controller
                        height, width, channels = current_frame.shape
                        ik_controller = IKController(image_height=height, image_width=width, plot_results=True)

                        chest = next((o for o in found_limbs if o.label == "chest"), None)
                        chest_x, chest_y = chest.get_center()
                        head = next((o for o in found_limbs if o.label == "head"), None)
                        head_x, head_y = head.get_center()
                        ik_controller.set_head_to_chest(object_tracker.calculate_distance(chest_x, chest_y, head_x, head_y))
                        has_found_limbs = True

                    cv2.imshow("Result", current_frame)
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