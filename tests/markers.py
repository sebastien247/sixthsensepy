import numpy as np
import cv2
import time
import math

class Marker:

    def __init__(self, hue):
        self.hue = hue
        self.lower_hsv_range = np.array([max(0, hue / 2 - 5), 0, 0], dtype=np.uint8)
        self.upper_hsv_range = np.array([min(180, hue / 2 + 5), 255, 255], dtype=np.uint8)
        self.moment = None
        self.contour = None
        self.timestamp_last_detected = -1

    @property
    def area(self):
        if self.contour is None:
            return -1
        return cv2.contourArea(self.contour)

    @property
    def centroid(self):
        if self.moment is None:
            return -1, -1
        cx = self.moment['m10'] / self.moment['m00']
        cy = self.moment['m01'] / self.moment['m00']
        return cx, cy

class MarkersDetector:

    def __init__(self, markers):
        self.markers = tuple(markers)

    def filter_contour(self, contour):
        # TODO: Check that the contour is not too complex and looks like a circle / square
        contourArea = cv2.contourArea(contour)
        return 50 < contourArea < 1000

    def eval_moment(self, moment, contour, marker):

        if marker.moment is not None:
            # Compute difference with the previous position / area of the marker to determine similarity
            cx = moment['m10'] / moment['m00']
            cy = moment['m01'] / moment['m00']

            mcx, mcy = marker.centroid

            area = cv2.contourArea(contour)

            marker_area = cv2.contourArea(marker.contour)

            # TODO: Compute the real variance for position / area thanks to empirical tests
            s_cx = 10
            s_cy = 9
            s_area = 50

            # Mahalanobis distance
            return math.sqrt((cx - mcx)**2/s_cx + (cy - mcy)**2/s_cy + (area - marker_area)**2/s_area)
        else:
            # Only use the area as the evalued feature regards

            # TODO: Compute the real usual area
            best_area = 200

            return abs(cv2.contourArea(contour) - best_area)

    def detect(self, frame):

        # Reduce image size to decrease noise and time computation
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        results = []

        for marker in self.markers:
            mask = cv2.inRange(frame_hsv, marker.lower_hsv_range, marker.upper_hsv_range)

            binary_img = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)
            binary_img = cv2.cvtColor(binary_img, cv2.COLOR_BGR2GRAY)
            _, binary_img = cv2.threshold(binary_img, 127, 255, cv2.THRESH_BINARY)

            struct_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            struct_open = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, struct_close)
            binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, struct_open)

            cv2.imshow(str(marker.hue), binary_img)
            contours, _ = cv2.findContours(binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            marker_moment = None
            marker_contour = None
            min_distance = float("inf")

            for contour in contours:
                if self.filter_contour(contour):
                    moment = cv2.moments(contour)
                    distance = self.eval_moment(moment, contour, marker)
                    if distance < min_distance:
                        min_distance = distance
                        marker_contour = contour
                        marker_moment = moment

            marker.moment = marker_moment
            marker.contour = marker_contour

            if marker_contour is not None:
                marker.timestamp_last_detected = time.time()

            results.append(marker.centroid)

        return results


if __name__ == '__main__':

    def test(color):
        img = cv2.imread("sample.png")

        hue = color // 2

        lower_range = np.array([max(0, hue - 5), 0, 0], dtype=np.uint8)
        upper_range = np.array([min(180, hue + 5), 255, 255], dtype=np.uint8)

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(img_hsv, lower_range, upper_range)

        binary_img = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)
        binary_img = cv2.cvtColor(binary_img, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(binary_img, 127, 255, cv2.THRESH_BINARY)

        cv2.imshow('sample', binary_img)
        cv2.waitKey(0)

    YELLOW = 50
    GREEN = 135
    BLUE = 200
    RED = 350

    RGB = [[0, 255, 255], [0, 255, 0], [255, 0, 0], [0, 0, 255]]

    yellow_marker = Marker(YELLOW)
    green_marker = Marker(GREEN)
    blue_marker = Marker(BLUE)
    red_marker = Marker(RED)

    marker_detector = MarkersDetector([yellow_marker, green_marker, blue_marker, red_marker])

    cap = cv2.VideoCapture(0)
    start = time.time()

    while 1:
        _, frame = cap.read()

        m = marker_detector.detect(frame)

        for i, (a, b) in enumerate(m):
            if a != -1:
                cv2.circle(frame, (int(a*4), int(b*4)), 30, RGB[i], thickness=3)

        cv2.imshow("frame", frame)
        cv2.waitKey(1)