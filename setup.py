from setuptools import setup, find_packages

setup(
	name='CAM2DistributedBackend',
	version='1.0-a0',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		'pyspark',
		'hdfs',
		'opencv-python',
		'numpy',
		'click',
	],
	entry_points='''
		[console_scripts]
		CAM2DistributedBackend=CAM2DistributedBackend:cli
	''',
) 
