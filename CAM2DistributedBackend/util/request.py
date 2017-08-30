"""Provide a class representing an analysis request for a list of cameras.

This module provides the `Request` class that represents a request for
analysis of a list of cameras. The class maintains essential parameters
needed to perform the analysis, such as the list of cameras to be analyzed,
the analysis frame rate, etc. The class also provides common methods needed to
handle requests, such as reading/writing requests from JSON files, splitting
requests, etc.

Class Listings
--------------
Request
    Represent an analysis request for a list of cameras.

"""

import json

from CAM2DistributedBackend.camera.camera import IPCamera, NonIPCamera
import constants


class Request(object):
    """Represent an analysis request for a list of cameras.

    This class represents an analysis request for a list of cameras. It
    maintains essential parameters needed to perform the analysis, such as
    the list of cameras to be analyzed, the analysis frame rate, etc. This
    class provides common methods needed to handle requests, such as
    reading/writing requests from JSON files, splitting requests, etc.

    Attributes
    ----------
    submission_id : int
        The id of the submission to which this request belong.
    interval : float
        The interval between analyzing every two successive frames in seconds.
        This is the inverse of the analysis frame rate. For example, if the
        `interval` = 0.2, this means that the analysis frame rate is 5 frames
        per second, i.e. the submitted analysis program will be invoked 5
        times every one second.
    duration : float
        The total analysis duration in seconds. For example, if `duration` =
        60, this means that the submitted analysis program will be invoked
        for 1 minute (at the appropriate frame rate according to the
        `interval` attribute).
    snapshots_to_keep : int
        The number of most recent snapshots available to the analysis program.
        For example, if `snapshots_to_keep` = 1, the system will maintain only
        the most recent snapshot from every camera. If `snapshots_to_keep` =
        10, the system will maintain the most recent 10 snapshots at any
        point of time.
    is_video: bool
        The way that the system will communicate with the cameras. Is it
        video (high frame rates)? or snapshots (low frame rates)?
    cameras : list of `Camera`
        The list of cameras to be analyzed.

    Methods
    -------
    __init__()
        Initialize a default empty instance of `Request`.

    """

    def __init__(self, file_name):

        """Initialize the request using a JSON file.

        This method initializes the request using the information from
        a JSON file.

        Parameters
        ----------
        file_name : str
            The file name of the input JSON file.

        See Also
        --------
        write_to_file(file_name) : Write the request to a JSON file.

        """

        # Load the JSON file with the request information.
        with open(file_name) as f:
            request = json.load(f)

        # Set the request attributes to the information extracted from
        # the JSON object.
        self.interval = request[constants.INTERVAL_ATTRIBUTE]
        self.duration = request[constants.DURATION_ATTRIBUTE]
        self.snapshots_to_keep = request[constants.SNAPSHOTS_TO_KEEP_ATTRIBUTE]
        self.is_video = request[constants.IS_VIDEO_ATTRIBUTE]
        self.analysis_class = request[constants.ANALYSIS_CLASS_ATTRIBUTE]
        self.timestamp = request[constants.TIMESTAMP_ATTRIBUTE]

        # Construct the list of `Camera` objects using the information
        # extracted from the JSON object.
        self.cameras = []
        # For all the cameras in the JSON object:
        for camera in request[constants.CAMERAS_ATTRIBUTE]:

            # The `type` field indicates the types of the camera.
            if camera[constants.CAMERA_TYPE_ATTRIBUTE] == \
                    constants.CAMERA_TYPE_IP:
                # If it is an IP camera, Initialize an `IPCamera` instance
                # with the associated information, and add it to the
                # `cameras` list.
                ip_camera = IPCamera(
                    camera[constants.CAMERA_KEY_ATTRIBUTE],
                    camera[constants.CAMERA_IP_ATTRIBUTE],
                    camera[constants.CAMERA_SNAPSHOT_PATH_ATTRIBUTE],
                    camera[constants.CAMERA_MJPG_PATH_ATTRIBUTE],
                    camera[constants.CAMERA_PORT_ATTRIBUTE],
                    camera[constants.CAMERA_LATITUDE_ATTRIBUTE],
                    camera[constants.CAMERA_LONGITUDE_ATTRIBUTE])
                self.cameras.append(ip_camera)

            elif camera[constants.CAMERA_TYPE_ATTRIBUTE] == \
                    constants.CAMERA_TYPE_NON_IP:
                # If it is a non-IP camera, Initialize a `NonIPCamera`
                # instance with the associated information, and add it to the
                # `cameras` list.
                non_ip_camera = NonIPCamera(
                    camera[constants.CAMERA_KEY_ATTRIBUTE],
                    camera[constants.CAMERA_SNAPSHOT_URL_ATTRIBUTE],
                    camera[constants.CAMERA_LATITUDE_ATTRIBUTE],
                    camera[constants.CAMERA_LONGITUDE_ATTRIBUTE])
                self.cameras.append(non_ip_camera)
