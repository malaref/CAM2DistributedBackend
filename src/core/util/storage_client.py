"""Provide a storage client to save results to persistent storage

Class Listings
--------------
StorageClient
    Represent a storage client that supports saving results to HDFS

"""

from hdfs import InsecureClient

import numpy, cv2, uuid, os

class StorageClient(object):
    
    """Represent a storage client that supports saving results to HDFS

    Methods
    -------
    save(self, file_name, result)
        Save results permanently to persistent storage.

    """

    def __init__(self, username, submission_id, camera_id, namenode_ip='localhost', namenode_port='50070'):
        """Initialize an internal client

        This constructor initializes an HDFS client.

        """

        self._internal_client = InsecureClient('http://{0}:{1}'.format(namenode_ip, namenode_port), root='/'.join(['/users', username, submission_id, camera_id]))
        
    def save(self, file_name, result):
        """Save results permanently to persistent storage.

        This method saves results permanently to persistent storage so that they
        can be retrieved by the user later. This method currently accepts results as
        numpy.ndarray. If an instance with any other type is passed, the method
        will save the string representation of the instance. This enables the method
        to save strings, integers, and other primitive data types.

        Parameters
        ----------
        file_name : str
            The file name to be used to save the results.
        result : object
            The results to be saved. The `result` can be numpy.ndarray.
            If an instance with any other type is passed, the method will
            save the string representation of the instance. This enables the
            method to save strings, integers, and other primitive data types.

        """

        # If the result is an OpenCV image, save it as an image.
        if (isinstance(result, numpy.ndarray)):
            # TODO Make this to a temp directory using os.path
            temp_file_name = str(uuid.uuid4()) + file_name.replace('/', '')
            cv2.imwrite(temp_file_name, result)
            self._internal_client.upload(file_name, temp_file_name)
            os.remove(temp_file_name)
        # Else, save the string representation of the object in a text file.
        else:
            self._internal_client.write(file_name, str(result))
