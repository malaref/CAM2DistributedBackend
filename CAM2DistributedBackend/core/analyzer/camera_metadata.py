"""Provide a class representing the metadata of a single camera.

This module provides a class that represents the metadata of a single camera.
Metadata currently includes the unique camera ID and the geographical location
of the camera.

Class Listings
--------------
CameraMetadata
    Represent the metadata of a single camera.

"""


class CameraMetadata(object):

    """Represent the metadata of a single camera.

    This class represents the metadata of a single camera. Metadata
    currently includes the unique camera ID and the geographical location of
    the camera.

    Attributes
    ----------
    camera_id : int
        The camera ID. This ID is unique, i.e. there are no cameras with
        the same ID. The ID is also fixed, i.e. any camera in the system
        will never change its ID.
    latitude : float
        The approximate latitude of the camera geographical location.
    longitude : float
        The approximate longitude of the camera geographical location.

    Methods
    -------
    __init__(self, camera_id):
        Initialize a `CameraMetadata` instance.

    """

    def __init__(self, camera_id, latitude, longitude):

        """Initialize a `CameraMetadata` instance.

        This constructor initializes a `CameraMetadata` instance using the
        camera ID.

        Parameters
        ----------
        camera_id : int
            The camera ID. This ID is unique, i.e. there are no cameras with
            the same ID. The ID is also fixed, i.e. any camera in the system
            will never change its ID.
        latitude : float
            The latitude of the camera.
        longitude : float
            The longitude of the camera.

        """

        # Set the instance attributes.
        self.camera_id = camera_id
        self.latitude = latitude
        self.longitude = longitude