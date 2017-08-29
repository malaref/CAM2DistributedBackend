from setuptools import setup

setup(
    name='CAM2DistributedBackend',
    version='1.0-a0',
    packages=['CAM2DistributedBackend'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'hdfs',
    ],
	scripts=['bin/cam2-backend'],
) 
