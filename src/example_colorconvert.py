# -*- coding: utf-8 -*-
"""
Example to show the extended usage of color conversion functionality in pco.Camera().
The example shows the various color and pseudocolor formats that are available
"""
import os
import pco
import numpy as np
import cv2
import traceback
import logging

logger = logging.getLogger("pco")
logger.setLevel(logging.INFO)
logger.addHandler(pco.stream_handler)


def main():

    image_count = 10

    with pco.Camera() as cam:

        cam.default_configuration()
        cam.exposure_time = 0.01

        user_file_path = input("Enter file path where images should go: ")
        # assert(os.path.exists(user_file_path))

        if not cam.is_color:
            user_lut_file = input("Enter file path of the LUT file you want to use: ")
            if not user_lut_file:
                user_lut_file = "./lut/LUT_blue.lt4"
            assert (os.path.exists(user_lut_file))

            conv_ctrl = cam.get_convert_control("BGR8")
            conv_ctrl["lut_file"] = user_lut_file
            cam.set_convert_control("BGR8", conv_ctrl)

        cam.configuration = {"timestamp": "binary & ascii"}

        cam.record(image_count, mode="sequence")
        cam.wait_for_first_image()

        img_m, meta = cam.image(0, data_format='Mono16', crop=None)  # (1,1,2048,2048) )
        print(
            f'{"recorder num: "}{meta["recorder image number"]}{", camera num: "}{meta["timestamp"]["image counter"]}')
        print(f'{"dimensions: "}{img_m.shape}{", data_format: "}{meta["data format"]}')
        cv2.imwrite(user_file_path+"/img_Mono16.tif", img_m)

        if not cam.is_color:
            img_m, meta = cam.image(0, data_format='BGR8')
            cam.load_lut("BGR8", user_lut_file)

        for i in range(image_count):
            img_m, meta = cam.image(i, data_format='bgra', crop=None)

            print(
                f'{"recorder num: "}{meta["recorder image number"]}{", camera num: "}{meta["timestamp"]["image counter"]}')
            print(f'{"dimensions: "}{img_m.shape}{", data_format: "}{meta["data format"]}')
            # cv2 expects BGR image data
            cv2.imwrite(user_file_path+"/img_"+str(i)+".tif", cv2.cvtColor(img_m, cv2.COLOR_BGRA2BGR))

        img_m, meta = cam.image(3, data_format='bgr', crop=None)
        print(
            f'{"recorder num: "}{meta["recorder image number"]}{", camera num: "}{meta["timestamp"]["image counter"]}')
        print(f'{"dimensions: "}{img_m.shape}{", data_format: "}{meta["data format"]}')
        cv2.imwrite(user_file_path+"/img_BGR8.tif", img_m)

        if cam.is_color:
            img_m, meta = cam.image(4, data_format='bgr16', crop=None)
            print(
                f'{"recorder num: "}{meta["recorder image number"]}{", camera num: "}{meta["timestamp"]["image counter"]}')
            print(f'{"dimensions: "}{img_m.shape}{", data_format: "}{meta["data format"]}')
            cv2.imwrite(user_file_path+"/img_BGR16.tif", img_m)

        img_avg = cam.image_average(data_format='bgr', crop=None)
        cv2.imwrite(user_file_path+"/img_avg.tif", img_avg)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(traceback.format_exc())
