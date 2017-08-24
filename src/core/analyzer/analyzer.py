"""Provide a base class for any submitted analysis class.

This module provides the base class that any submitted analysis class must
inherit from. The class provides subclasses with methods to get the new frames
and their metadata. The class also provides a method to permanently save
analysis results.

Class Listings
--------------
Analyzer
    Represent a base class for any submitted analysis class.

"""

import numpy
import cv2

class Analyzer(object):

    """Represent a base class for any submitted analysis class.

    This class represents the base class that any submitted analysis class must
    inherit from. It provides subclasses with methods to get the new frames
    and their metadata. It also provides a method to permanently save
    analysis results.

    Methods
    -------
    get_frame(self, frame_index=0)
        Get a recent frame.
    get_frame_metadata(self, frame_index=0)
        Get the metadata of a recent frame.
    save(self, file_name, result)
        Save results permanently to disk.

    """

    def __init__(self, id):

        """Initialize a default `Analyzer` instance.

        This constructor initializes a default empty `Analyzer` instance.

        """

        self.id = id
        self._frames = []
        self._frames_metadata = []

    def _add_frame(self, frame, frame_metadata, frames_limit):

        """Add a new frame with its metadata.

        This method adds a new frame to the list of most recent frames. It
        also adds the metadata of the new frame to the list of frames
        metadata. The method ensures that the length of the frames list does
        not exceed `frames_limit`.

        Parameters
        ----------
        frame : numpy.ndarray
            The new frame to be added.
        frame_metadata : `FrameMetadata`
            The metadata of the new frame.
        frames_limit : int
            The maximum number of old frames to keep.

        """

        # Add the new frame at the front of the frames list.
        self._frames.insert(0, frame)

        # Add the new frame metadata at the front of the frames metadata list.
        self._frames_metadata.insert(0, frame_metadata)

        # If the length of the frames list exceeds `frames_limit`, remove the
        #  last element of both the frames list and the frames metadata list.
        if len(self._frames) > frames_limit:
            self._frames.pop()
            self._frames_metadata.pop()

    def get_frame(self, frame_index=0):

        """Get a recent frame.

        This methods gets a recent frame based on the input `frame_index`
        optional parameter. The `frame_index` parameter specifies how recent
        the returned frame is. If `frame_index` = 0 (or not specified),
        the method returns the most recent frame. If `frame_index` = i,
        the method returns the ith most recent frame.

        Parameters
        ----------
        frame_index : index, optional
            The recency index of the returned frame. It specifies how recent
            the returned frame is. If `frame_index` = 0 (or not specified),
            the method returns the most recent frame. If `frame_index` = i,
            the method returns the ith most recent frame.

        Returns
        -------
        numpy.ndarray
            The recent frame specified by the `frame_index`.

        """

        return self._frames[frame_index]

    def get_frame_metadata(self, frame_index=0):

        """Get the metadata of a recent frame.

        This methods gets the metadata of a recent frame based on the input
        `frame_index`  optional parameter. The `frame_index` parameter
        specifies how recent  the frame is. If `frame_index` = 0 (or not
        specified), the method returns the metadata of the most recent frame.
        If `frame_index` = i, the method returns the metadata of the ith most
        recent frame.

        Parameters
        ----------
        frame_index : index, optional
            The recency index of the frame. It specifies how recent the
            returned frame is. If `frame_index` = 0 (or not specified),
            the method returns the metadata of the most recent frame. If
            `frame_index` = i, the method returns the metadata of the ith most
            recent frame.

        Returns
        -------
        numpy.ndarray
            The recent frame specified by the `frame_index`.

        """

        return self._frames_metadata[frame_index]
    
    # TODO use a distributed file system
    def save(self, file_name, result):

        """Save results permanently to disk.

        This method saves results permanently to disk so that they can be
        retrieved by the user later. This method currently accepts results as
        PIL.Image.Image, numpy.ndarray. If an instance with any other type is
        passed, the method will save the string representation of the instance.
        This enables the method to save strings, integers, and other
        primitive data types.

        Parameters
        ----------
        file_name : str
            The file name to be used to save the results.
        result : object
            The results to be saved. The `result` can be PIL.Image.Image,
            numpy.ndarray. If an instance with any other type is passed,
            the method will save the string representation of the instance.
            This enables the method to save strings, integers, and other
            primitive data types.

        """
        
        # Construct the file path of the results file.
        file_path = 'output/' + str(self.id) + '__' + file_name

        # If the result is an OpenCV image, save it as an image.
        if (isinstance(result, numpy.ndarray)):
            cv2.imwrite(file_path, result)
        # Else, save the string representation of the object in a text file.
        else:
            with open(file_path, 'a') as f:
                f.write(str(result))


    def initialize(self):

        """Handle the event of analysis initialization.

        This method is the event handler of initializing the analysis method.
        The method is invoked once at the beginning of the analysis process.
        This method should be overridden by a subclass if needed, and its
        implementation in the subclasses depends on the desired analysis method.

        Notes
        -----
        This method does nothing in the parent `Analyzer` class.

        """

        pass

    def on_new_frame(self):

        """Handle the event of the arrival of a new frame.

        This method is the event handler of the arrival of a new frame. The
        method  is invoked on the arrival of any new frame. This method is an
        abstract method that must be overridden by any subclass. The
        implementation of this method in the subclasses depends on the
        desired analysis method.

        Raises
        ------
        NotImplementedError
            If the method is not overridden in the subclass.

        """

        # This code is unreachable if the method `on_new_frame` is overridden
        # in the subclasses as required.
        raise NotImplementedError('on_new_frame handler must be implemented.')

    def finalize(self):

        """Handle the event of analysis finalization.

        This method is the event handler of finalizing the analysis method.
        The method is invoked once at the end of the analysis process. This
        method should be overridden by a subclass if needed, and its
        implementation in the subclasses depends on the desired analysis method.

        Notes
        -----
        This method does nothing in the parent `Analyzer` class.

        """
        
        pass
