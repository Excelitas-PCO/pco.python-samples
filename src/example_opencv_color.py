# -*- coding: utf-8 -*-
"""
Example showing how to apply and show opencv colormaps on images from pco.Camera.
"""
import logging
import cv2
import numpy as np
import pco


logger = logging.getLogger("pco")
logger.setLevel(logging.INFO)
logger.addHandler(pco.stream_handler)

def main():

    with pco.Camera() as cam:

        # cv2.namedWindow("pco.python", cv2.WINDOW_NORMAL)

        cam.configuration = {
            'timestamp': 'binary & ascii',
            'exposure time': 10e-3,
        }

        cam.record(4, 'ring buffer')

        while True:

            cam.wait_for_new_image()
            image, _ = cam.image(0xFFFFFFFF, data_format='mono8')

            im_color = cv2.applyColorMap(image, cv2.COLORMAP_DEEPGREEN)
            cv2.imshow('pco.python', im_color)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam.stop()
                break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
