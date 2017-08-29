"""Provide a class representing the metadata of a single frame.

This module provides a class that represents the metadata of a single frame
captured by a a single camera at a specific time. The class provides the
metadata of  the camera that captured the frame, the sequence number of the
frame,  the timestamp of the frame.

Class Listings
--------------
FrameMetadata
    Represent the metadata of a single frame captured by a camera.

"""

import datetime


class FrameMetadata(object):

    """Represent the metadata of a single frame captured by a camera.

    This class represents the metadata of a single frame captured by a
    a single camera at a specific time. The class provides the metadata of
    the camera that captured the frame, the sequence number of the frame,
    the timestamp of the frame.

    Attributes
    ----------
    camera_metadata : `CameraMetadata`
        The metadata of the camera from which the frame is captured.
    sequence_num : int
        The sequence number of the frame. The sequence number is equal to 0
        for the very first frame sent to the analysis program during the
        initialization stage (the `initialize` event). The sequence
        number is then incremented for every new frame sent to the
        analysis program during the processing stage (the `on_new_frame`
        event). For example, if the current `sequence_num` = 31,
        this means that this frame is the 31st frame sent to the
        `on_new_frame` event, in other words: the `on_new_frame` event
        has been invoked 31 times.
    timestamp : float
        The timestamp of the frame since the epoch in seconds.
    datetime : datetime.datetime
        The date/time of the frame.

    Methods
    -------
    __init__(self, camera_metadata, sequence_num, timestamp):
        Initialize a `FrameMetadata` instance.

    """

    def __init__(self, camera_metadata, sequence_num, timestamp):

        """Initialize a `FrameMetadata` instance.

        This constructor initializes a `FrameMetadata` instance using the
        metadata information: camera metadata, sequence number, and timestamp.

        Parameters
        ----------
        camera_metadata : `CameraMetadata`
            The metadata of the camera from which the frame is captured.
        sequence_num : int
            The sequence number of the frame. The sequence number is equal to 0
            for the very first frame sent to the analysis program during the
            initialization stage (the `initialize` event). The sequence
            number is then incremented for every new frame sent to the
            analysis program during the processing stage (the `on_new_frame`
            event). For example, if the current `sequence_num` = 31,
            this means that this frame is the 31st frame sent to the
            `on_new_frame` event, in other words: the `on_new_frame` event
            has been invoked 31 times.
        timestamp : float
            The timestamp of the frame since the epoch in seconds.

        """

        # Set the instance attributes.
        self.camera_metadata = camera_metadata
        self.sequence_num = sequence_num
        self.timestamp = timestamp

    @property
    def datetime(self):

        """Get the date/time of the frame.

        This property gets the date/time in which the frame is captured.

        Returns
        -------
        datetime.datetime
            The date/time in which the frame is taken by the camera.

        """

        # Convert the `timestamp` instance attribute to datetime.
        return datetime.datetime.fromtimestamp(self.timestamp)