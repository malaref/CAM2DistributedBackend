"""The driver program of Spark

This module resembles the driver program of an analysis submission.

"""

from pyspark import SparkContext, SparkConf

from camera.camera import IPCamera, StreamFormat
from analyzer.camera_metadata import CameraMetadata
from analyzer.frame_metadata import FrameMetadata
import time

# TODO Make this configurable
analysis_duration = 20
frames_limit = 5

def run_analyzer(camera):
    # Initialize the analyzer
    from user_analyzer import MyAnalyzer
    analyzer = MyAnalyzer(camera.id)
    analyzer.initialize()

    # Initialize the camera
    camera.open_stream(StreamFormat.MJPEG)
    
    # Set up initial meta-data
    start_time = time.time()
    frame_sequence_num = 0
    camera_metadata = CameraMetadata(camera.id, camera.latitude, camera.longitude)

    # Analysis loop
    while time.time() - start_time < analysis_duration:
        frame, frame_size = camera.get_frame()
        frame_timestamp = time.time()
        frame_metadata = FrameMetadata(camera_metadata, frame_sequence_num, frame_timestamp)
        analyzer._add_frame(frame, frame_metadata, frames_limit)
        analyzer.on_new_frame()
        frame_sequence_num += 1

    # Finalize
    camera.close_stream()
    analyzer.finalize()
    
# Initialize Spark
conf = SparkConf().setAppName('CAM2 Analysis')
ctx = SparkContext(conf=conf)

# Prepare the cameras
# TODO Make this configurable
cameras = [
    IPCamera(1, '89.29.49.6',         '/axis-cgi/jpg/image.cgi', '/axis-cgi/mjpg/video.cgi'),
    IPCamera(2, '128.104.181.37', '/axis-cgi/jpg/image.cgi', '/axis-cgi/mjpg/video.cgi'),
    IPCamera(3, '128.210.129.12', '/axis-cgi/jpg/image.cgi', '/axis-cgi/mjpg/video.cgi')]

# Submit the analysis job
distributedCameras = ctx.parallelize(cameras)
distributedCameras.foreach(run_analyzer)
