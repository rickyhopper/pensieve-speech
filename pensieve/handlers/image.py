import cv2
import cv2.cv as cv
import numpy as np
from threading import Thread

from .base_handler import BaseHandler
from ..helpers import ok, invalidValue, checkField, MessageError


class Image(BaseHandler):
    image = None

    def __init__(self):
        self.displayThread = Thread(target=self.display)
        self.displayThread.daemon = True
        self.displayThread.start()

    # Display and update image in a window
    def display(self):
        cv2.namedWindow("Image")
        while True:
            if self.image is not None:
                cv2.imshow("Image", self.image)
            cv2.waitKey(10)

    def handle(self, header, data):
        try:
            height = checkField(header, 'height')
            width = checkField(header, 'width')
            format = checkField(header, 'format')
        except MessageError as e:
            return e.json

        # is image in RGB format?
        if 'RGB' != format:
            return invalidValue('format', format, 'RGB')

        # Assuming 3-channel image
        image = np.ndarray(shape=(height, width, 3), dtype=np.uint8, buffer=data)
        image = cv2.cvtColor(image, cv.CV_RGB2BGR)
        self.image = image
        return ok('image', 'ack')
