# -*- coding: utf-8 -*-
"""
Example showing how images from pco.Camera can be displayed via opencv-python.
Additionally we activate auto exposure functionality
"""
import logging
import cv2
import pco


logger = logging.getLogger("pco")
logger.setLevel(logging.INFO)
logger.addHandler(pco.stream_handler)

def main():

    with pco.Camera() as cam:

        cam.configuration = {'timestamp': 'binary & ascii',
                             'roi': (1, 1, 1024, 1024)}
        cam.configure_auto_exposure(region_type='balanced', 
                                    min_exposure_s=1e-3,
                                    max_exposure_s=50e-3)
        
        cam.record(10, 'ring buffer')
        cam.auto_exposure_on()
        while True:
            cam.wait_for_new_image()
            image, _ = cam.image(0xFFFFFFFF)
            cv2.imshow('pco.python', image)

            mean = image.mean()
            exp_time = cam.exposure_time
            print('Mean: {:6.1f}, Exposure time: {:8.6f}'.format(mean, exp_time))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam.stop()
                cam.auto_exposure_off()
                break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
