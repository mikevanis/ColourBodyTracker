import cv2
import imutils
import sys
import argparse
sys.path.insert(0, 'CameraController')
from CameraController import CameraController
from ShapeDetector import ShapeDetector
from MarkerFinder import MarkerFinder

parser = argparse.ArgumentParser()
parser.add_argument("--test_video")
args = parser.parse_args()

sd = ShapeDetector()
marker_finder = MarkerFinder(show_mask=True)

if __name__ == '__main__':
    if args.test_video is None:
        cam = CameraController(width=600, height=400)
        cam.start()

        try:
            while True:
                current_frame = cam.get_image()

                if current_frame is not None:
                    points = marker_finder.find(current_frame)

                    for p in points:
                        cv2.circle(current_frame, p, 5, (255, 0, 255), -1)

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
        cap = cv2.VideoCapture(args.test_video)
        while(cap.isOpened()):
            ret, current_frame = cap.read()
            current_frame = imutils.resize(current_frame, 600)
            current_frame = imutils.rotate_bound(current_frame, 270)

            points = marker_finder.find(current_frame)

            for p in points:
                cv2.circle(current_frame, p, 5, (255, 0, 255), -1)

            cv2.imshow("Result", current_frame)
            key = cv2.waitKey(1)

            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
