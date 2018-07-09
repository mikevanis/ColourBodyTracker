import cv2
import imutils
import sys
sys.path.insert(0, 'CameraController')
from CameraController import CameraController
from ShapeDetector import ShapeDetector

sd = ShapeDetector()

if __name__ == '__main__':
    cam = CameraController(width=600, height=400)
    cam.start()

    try:
        while True:
            current_frame = cam.get_image()

            if current_frame is not None:
                blurred = cv2.GaussianBlur(current_frame, (11, 11), 0)
                blurred = (255-blurred)
                frame_to_thresh = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
                lower_cyan = (85-10, 70, 50)
                upper_cyan = (85+10, 255, 255)
                thresh = cv2.inRange(frame_to_thresh, lower_cyan, upper_cyan)
                thresh = cv2.erode(thresh, None, iterations=2)
                thresh = cv2.dilate(thresh, None, iterations=2)

                _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in cnts:
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    if radius > 10:
                        cv2.circle(current_frame, center, 5, (255, 0, 255), -1)
                        shape = sd.detect(c)
                        cX = int((M["m10"] / M["m00"]))
                        cY = int((M["m01"] / M["m00"]))
                        cv2.putText(current_frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

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
