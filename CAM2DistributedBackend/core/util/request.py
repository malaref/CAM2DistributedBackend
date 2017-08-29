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

from camera.camera import IPCamera, NonIPCamera
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
    read_from_file(file_name)
        Initialize the request using a JSON file.
    write_to_file(file_name)
        Write the request to a JSON file.
    extract_request_with_limit(cameras_limit)
        Extract a new request with a limited number of cameras.

    """

    def __init__(self):

        """Initialize a default empty instance of `Request`."""

        # Set the instance attributes to None, or empty list.
        self.submission_id = None
        self.interval = None
        self.duration = None
        self.snapshots_to_keep = None
        self.is_video = None
        self.cameras = []
        self.program = None
        self.timestamp = None

    def read_from_file(self, file_name):

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
        self.submission_id = request[constants.SUBMISSION_ID_ATTRIBUTE]
        self.interval = request[constants.INTERVAL_ATTRIBUTE]
        self.duration = request[constants.DURATION_ATTRIBUTE]
        self.snapshots_to_keep = request[constants.SNAPSHOTS_TO_KEEP_ATTRIBUTE]
        self.is_video = request[constants.IS_VIDEO_ATTRIBUTE]
        self.program = request[constants.PROGRAM_ATTRIBUTE]
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

    def write_to_file(self, file_name):

        """Write the request to a JSON file.

        This method writes the information of the request to a JSON file.

        Parameters
        ----------
        file_name : str
            The file name of the output JSON file.

        See Also
        --------
        read_from_file(file_name) : Initialize the request using a JSON file.

        """

        # Construct a list of cameras: each camera entry is a dictionary that
        # has the information about this camera.
        cameras = []
        # For all the cameras in the request:
        for camera in self.cameras:
            # Each camera entry (dictionary) has different fields based on
            # the type of the camera.
            if isinstance(camera, IPCamera):
                cameras.append(
                    {constants.CAMERA_TYPE_ATTRIBUTE: constants.CAMERA_TYPE_IP,
                     constants.CAMERA_KEY_ATTRIBUTE: camera.id,
                     constants.CAMERA_IP_ATTRIBUTE: camera.ip,
                     constants.CAMERA_SNAPSHOT_PATH_ATTRIBUTE:
                         camera.image_path,
                     constants.CAMERA_MJPG_PATH_ATTRIBUTE: camera.mjpeg_path,
                     constants.CAMERA_PORT_ATTRIBUTE: camera.port,
                     constants.CAMERA_LATITUDE_ATTRIBUTE: camera.latitude,
                     constants.CAMERA_LONGITUDE_ATTRIBUTE: camera.longitude})

            elif isinstance(camera, NonIPCamera):
                cameras.append(
                    {constants.CAMERA_TYPE_ATTRIBUTE:
                         constants.CAMERA_TYPE_NON_IP,
                     constants.CAMERA_KEY_ATTRIBUTE: camera.id,
                     constants.CAMERA_SNAPSHOT_URL_ATTRIBUTE:
                         camera.url,
                     constants.CAMERA_LATITUDE_ATTRIBUTE: camera.latitude,
                     constants.CAMERA_LONGITUDE_ATTRIBUTE: camera.longitude})

        # Construct a dictionary with all the information about the request,
        # including the list of cameras constructed above.
        request = {constants.SUBMISSION_ID_ATTRIBUTE: self.submission_id,
                   constants.INTERVAL_ATTRIBUTE: self.interval,
                   constants.DURATION_ATTRIBUTE: self.duration,
                   constants.SNAPSHOTS_TO_KEEP_ATTRIBUTE:
                       self.snapshots_to_keep,
                   constants.IS_VIDEO_ATTRIBUTE: self.is_video,
                   constants.CAMERAS_ATTRIBUTE: cameras,
                   constants.PROGRAM_ATTRIBUTE: self.program,
                   constants.TIMESTAMP_ATTRIBUTE: self.timestamp}

        # Dump the dictionary of the request to a JSON file.
        with open(file_name, 'w') as f:
            json.dump(request, f, sort_keys=True, indent=4)

    def split_into(self, requests_count):

        """Split the request into multiple requests.

        This method splits the request into multiple requests without
        affecting the original request. The list of cameras is split equally
        among the new requests. All other parameters of the requests (e.g.
        `submission_id`) stay the same as the original request.

        Parameters
        ----------
        requests_count : int
            The number of output requests needed.

        Returns
        -------
        requests : list of `Request`
            The list of requests resulting from splitting the original
            request. All list elements have the same parameters, except the
            list of cameras which is split equally among the requests.

        See Also
        --------
        extract_request_with_limit : Extract a new request with a limited
        number of cameras.

        """

        requests = []
        # Split the list of cameras into `requests_count` chunks equally.
        # Each chunk will have not more than len(self.cameras)/requests_count.
        # For each chunk of cameras:
        for cameras_chunk in [self.cameras[i::requests_count]
                              for i in xrange(requests_count)]:

            if len(cameras_chunk) == 0:
                break

            # Initialize a `Request` instance with the same parameters as the
            # original request, except the list of cameras which will be the
            # cameras chunk.
            request = Request()
            request.submission_id = self.submission_id
            request.interval = self.interval
            request.duration = self.duration
            request.snapshots_to_keep = self.snapshots_to_keep
            request.is_video = self.is_video
            request.cameras = cameras_chunk
            request.program = self.program
            request.timestamp = self.timestamp
            requests.append(request)

        return requests

    def extract_request_with_limit(self, cameras_limit):

        """Extract a new request with a limited number of cameras.

        This method extracts a list of `cameras_limit` cameras from the
        list of cameras in the request, and creates a new request with the
        extracted list of cameras. All other parameters of the new request (
        e.g. `submission_id`) stay the same as the original request.

        Parameters
        ----------
        requests_count : int
            The number of output requests needed.

        Returns
        -------
        requests : list of `Request`
            The list of requests resulting from splitting the original
            request. All list elements have the same parameters, except the
            list of cameras which is split equally among the requests.

        See Also
        --------
        extract_request_with_limit : Split the request into multiple requests.

        Notes
        -----
        This method removes the extracted list of cameras from the original
        request. For example, if a request has 40 cameras, and this method is
        invoked with a `cameras_limit` of 10, the number of cameras in the
        original request will become 30.

        The new list of cameras will be extracted from the beginning of the
        original list of cameras.

        """

        # Initialize a `Request` instance with the same parameters as the
        # original request, except the list of cameras.
        request = Request()
        request.submission_id = self.submission_id
        request.interval = self.interval
        request.duration = self.duration
        request.snapshots_to_keep = self.snapshots_to_keep
        request.is_video = self.is_video
        request.program = self.program
        request.timestamp = self.timestamp

        # Split the list of cameras into two halves: the first
        # `cameras_limit` cameras goes to the new request, and the second
        # half stays in the original request.
        request.cameras = self.cameras[:cameras_limit]
        self.cameras = self.cameras[cameras_limit:]

        return request

    def remove_cameras(self, cameras_num):
        last_cameras = self.cameras[-cameras_num:]
        self.cameras = self.cameras[0:-cameras_num]
        return last_cameras

    def add_cameras(self, cameras):
        self.cameras.extend(cameras)
