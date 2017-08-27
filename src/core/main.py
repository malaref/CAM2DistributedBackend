"""The driver program of Spark

This module resembles the driver program of an analysis submission.

"""

from pyspark import SparkContext, SparkConf

from camera.camera import IPCamera, StreamFormat
from util.request import Request
import time, sys

# Setting up the request
request = Request()
request.read_from_file(sys.argv[1]) # TODO Use argparse to make it cleaner

username = sys.argv[2] # TODO Use argparse to make it cleaner
master_url = 'spark://Exs:7077' # TODO make this configurable
								# For local mode: 'local[{}]'.format(len(cameras))
submission_id = request.submission_id
analysis_duration = request.duration
frames_limit = request.snapshots_to_keep
is_video = request.is_video

def run_analyzer(camera):
    # Necessary imports
    from user_analyzer import MyAnalyzer
    from util.storage_client import StorageClient
    from analyzer.camera_metadata import CameraMetadata
    from analyzer.frame_metadata import FrameMetadata
    
    # Initialize a storage client
    storage_client = StorageClient(username, submission_id, camera.id)
    
    # Initialize the analyzer
    analyzer = MyAnalyzer()
    analyzer._save = storage_client.save
    analyzer.initialize()

    # Initialize the camera
    if is_video:
        stream_format = StreamFormat.MJPEG
    else:
        stream_format = StreamFormat.IMAGE
    camera.open_stream(stream_format)
    
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

# Prepare the cameras
cameras = request.cameras

# Initialize Spark
conf = SparkConf().setAppName('CAM2 Analysis').setMaster(master_url).set('spark.cores.max', len(cameras))
ctx = SparkContext(conf=conf)

# Submit the analysis job
distributedCameras = ctx.parallelize(cameras, len(cameras))
distributedCameras.foreach(run_analyzer)
