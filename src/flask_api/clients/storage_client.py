from hdfs import InsecureClient

import tempfile, shutil

class StorageClient(object):
	
	@staticmethod
	def prepare_result_as_zip_file(username, submission_id, namenode_ip='localhost', namenode_port='50070'):
		client = InsecureClient('http://{0}:{1}'.format(namenode_ip, namenode_port))
		temp_directory = tempfile.mkdtemp() # TODO DRYing this pattern
		client.download('/'.join(['/users', username, str(submission_id)]), temp_directory)
		archive_name = shutil.make_archive(str(submission_id), 'zip', temp_directory)
		shutil.rmtree(temp_directory)
		return archive_name
