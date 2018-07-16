import cv2
import imutils
import sys
import argparse
from imutils.video import FileVideoStream
import time
sys.path.insert(0, 'CameraController')
from CameraController import CameraController
from VideoController import VideoController
from ShapeDetector import ShapeDetector
from MarkerFinder import MarkerFinder
from ObjectTracker import ObjectTracker
from ObjectTracker import TrackedObject

parser = argparse.ArgumentParser()
parser.add_argument("--test_video")
args = parser.parse_args()

sd = ShapeDetector()
marker_finder = MarkerFinder(show_mask=True, min_radius=4)
object_tracker = ObjectTracker()

found_limbs = None

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
                    if found_limbs is not None:
                        for limb in found_limbs:
                            cv2.putText(current_frame, limb.label, limb.get_center(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    else:
                        found_limbs = object_tracker.label_contours(contours)

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