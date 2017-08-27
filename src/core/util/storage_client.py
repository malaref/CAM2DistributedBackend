"""Provide a storage client to save results to persistent storage

Class Listings
--------------
StorageClient
    Represent a storage client that supports saving results to HDFS

"""

from hdfs import InsecureClient

import numpy, cv2, tempfile, os

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

        self._internal_client = InsecureClient('http://{0}:{1}'.format(namenode_ip, namenode_port), root='/'.join(['/users', username, str(submission_id), str(camera_id)]))
        
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

        # Make sure the file name is legit
        file_name = file_name.replace('/', '.')
        # If the result is an OpenCV image, save it as an image.
        if (isinstance(result, numpy.ndarray)):
            # Create temp files
            temp_directory = tempfile.mkdtemp()
            temp_image_path = os.path.join(temp_directory, file_name)
            cv2.imwrite(temp_image_path, result)
            self._internal_client.upload(file_name, temp_image_path, overwrite=True)
            # Remove temp files
            os.remove(temp_image_path)
            os.rmdir(temp_directory)
        # Else, save the string representation of the object in a text file.
        else:
            self._internal_client.write(file_name, str(result), overwrite=True)
