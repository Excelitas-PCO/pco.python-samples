"""
Example to show how images of pco.Camera can be transferred to a flask server to be used as webcam.
"""

import logging
import time
from flask import Flask,  Response, render_template_string
import cv2
import pco


logger = logging.getLogger("pco")
logger.setLevel(logging.DEBUG)
logger.addHandler(pco.stream_handler)


HTML = """
<!DOCTYPE html>
<html>
<head>
<title> {{ title }} </title>
<style>
body {background-color: ghostwhite; font-size: 100%;}
h1   {color: black; font-family: verdana;}
p    {color: black; font-family: verdana;}
</style>
</head>
<body>
<img src=https://www.pco.de/fileadmin/user_upload/company/pco_logo.png width="100">
<h1>  {{ title }}</h1>
<p> {{ camera_name }} </p>
<p> {{ camera_serial }} </p>
<img src="{{ url_for('video_feed') }}" width="800">
</body>
</html>"""


def make_web(cam):

    app = Flask(__name__)

    @app.route('/')
    def index():
        title = "Python Flask Example"
        camera_name = "Name: {}".format(cam.camera_name)
        camera_serial = "Serial: {}".format(cam.camera_serial)
        return render_template_string(
            HTML,
            title=title,
            camera_name=camera_name,
            camera_serial=camera_serial
        )

    def gen():
        while True:
            start = time.perf_counter()
            cam.wait_for_new_image()
            image, _ = cam.image(0xFFFFFFFF, data_format="Mono8")
            _, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            print("{:2.5f} s".format(time.perf_counter() - start))
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0', port=5000)


def main():

    with pco.Camera() as cam:
        cam.configuration = {
            "timestamp": 'binary & ascii'
        }
        cam.record(10, "ring buffer")
        cam.wait_for_first_image()

        make_web(cam)


if __name__ == "__main__":
    main()
