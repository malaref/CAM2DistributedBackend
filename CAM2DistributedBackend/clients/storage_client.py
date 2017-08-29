from hdfs import InsecureClient
from hdfs.util import HdfsError

import tempfile, shutil

def _get_path(username, submission_id):
	return '/'.join(['/users', username, str(submission_id)])

class StorageClient(object):
	
	def __init__(self, namenode_url):
		self._internal_client = InsecureClient(namenode_url)
	
	def prepare_result_as_zip_file(self, username, submission_id):
		temp_directory = tempfile.mkdtemp()
		try:
			self._internal_client.download(_get_path(username, submission_id), temp_directory)
		except HdfsError:
			pass
		archive_name = shutil.make_archive(str(submission_id), 'zip', temp_directory)
		shutil.rmtree(temp_directory)
		return archive_name
	
	def delete_result(self, username, submission_id):
		return self._internal_client.delete(_get_path(username, submission_id), recursive=True)
	
	def delete_user(self, username):
		return self._internal_client.delete('/'.join(['/users', username]), recursive=True)
