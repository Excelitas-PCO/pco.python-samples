# -*- coding: utf-8 -*-
"""
Example to show typical workflow for cameras with internal memory using pco.Camera()
The relevant record modes for this are \"camram ring\" and \"camram segment\"
"""

import logging
import time
import pco

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(pco.stream_handler)


def main():
    with pco.Camera() as cam:

        cam.default_configuration()

        cam.camram_allocation = [50, 20, 5]
        cam.switch_to_camram(3)

        print("camram segment {}: {} / {}".format(cam.camram_segment, cam.camram_num_images, cam.camram_max_images))

        cam.configuration = {
            'timestamp': 'binary & ascii',
            'metadata': 'on'
        }

        cam.record(cam.camram_max_images, "camram ring")
        cam.wait_for_first_image()
        i = 0
        starttime = time.perf_counter()

        while time.perf_counter() - starttime < 10:
            i = i+1
            image, meta = cam.image(0xFFFFFFFF)
            print("img {}: {}".format(i, meta["recorder image number"]))
            cam.wait_for_new_image()

        cam.stop()
        image, meta = cam.image(0)
        image, meta_end = cam.image(cam.camram_num_images - 1)
        print("CamRam ring buffer holds images from {} to {}".format(meta["timestamp bcd"]["image counter"], meta_end["timestamp bcd"]["image counter"]))

        cam.record(cam.camram_max_images, "camram segment")
        cam.wait_for_first_image()
        i = 0
        starttime = time.perf_counter()
        while cam.is_recording:
            i = i+1
            image, meta = cam.image(0xFFFFFFFF)
            print("img {}: {}".format(i, meta["recorder image number"]))
            cam.wait_for_new_image()


        image, meta = cam.image(0)
        image, meta_end = cam.image(cam.camram_max_images - 1)
        print("CamRam segment holds images from {} to {}".format(meta["timestamp bcd"]["image counter"], meta_end["timestamp bcd"]["image counter"]))
        
        print(image, type(image), image.shape)
        print(meta['timestamp'])
        print(meta['timestamp bcd'])

        print("camram segment {}: {} / {}".format(cam.camram_segment, cam.camram_num_images, cam.camram_max_images))


if __name__ == '__main__':
    main()
