"""Provide an API for the submitted analysis programs.

This package is responsible for providing an API for the submitted analysis
programs. Analysis programs are aware of only this package, and do not have
to learn any other aspects of the system. The package has different modules
to (i) provide the submitted analysis programs with the input frames and
their metadata, and (ii) allow the programs to save results permanently.

Module Listings
---------------
analyzer
    Provide a base class for any submitted analysis class.
frame_metadata
    Provide a class representing the metadata of a single frame.
camera_metadata
    Provide a class representing the metadata of a single camera.

"""