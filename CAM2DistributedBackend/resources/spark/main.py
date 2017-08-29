"""The driver program of Spark

This module resembles the driver program of an analysis submission.

"""

from pyspark import SparkContext, SparkConf

from camera.camera import IPCamera, StreamFormat
from util.request import Request
import time, argparse

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Spark submitter')
parser.add_argument('master_url', help='Spark master URL')
parser.add_argument('namenode_url', help='HDFS namenode URL')
parser.add_argument('username', help='username of the submitter')
parser.add_argument('submission_id', help='the id of the submission')
parser.add_argument('request_file', help='.json file')
args = parser.parse_args()

# Setting up the request
request = Request(args.request_file)

username = args.username
submission_id = args.submission_id
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
    storage_client = StorageClient(args.namenode_url, username, submission_id, camera.id)
    
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
master_url = args.master_url	# For local mode: 'local[{}]'.format(len(cameras))
conf = SparkConf().setAppName('CAM2 Analysis').setMaster(master_url).set('spark.cores.max', len(cameras))
ctx = SparkContext(conf=conf)

# Submit the analysis job
distributedCameras = ctx.parallelize(cameras, len(cameras))
distributedCameras.foreach(run_analyzer)
