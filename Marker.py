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