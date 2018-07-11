import cv2
import imutils
import sys
sys.path.insert(0, 'CameraController')
from CameraController import CameraController
from ShapeDetector import ShapeDetector
from MarkerFinder import MarkerFinder

sd = ShapeDetector()
marker_finder = MarkerFinder()

if __name__ == '__main__':
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
