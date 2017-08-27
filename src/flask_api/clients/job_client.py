from flask_api import database_client

import tempfile, os, json, subprocess, threading

class JobClient(object):
	
	def __init__(self, username, conf, analyzer_script):
		# Create temp files
		self._temp_directory = tempfile.mkdtemp()
		self._temp_conf_file_path = os.path.join(self._temp_directory, 'user_conf.json')
		self._temp_analyzer_script_path = os.path.join(self._temp_directory, 'user_analyzer.py')
		with open(self._temp_conf_file_path, 'w') as f:
			json.dump(conf, f, sort_keys=True, indent=4)
		analyzer_script.save(self._temp_analyzer_script_path)
		# Adding attributes
		self.username = username
		self.submissionId = conf['submission_id']
		# Submit the job
		self._job = subprocess.Popen('$SPARK_HOME/bin/spark-submit --py-files core/cam2.zip,{1} core/main.py {0} {2}'.format(self._temp_conf_file_path, self._temp_analyzer_script_path, self.username), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		threading.Thread(target=self._handle_stdout).start()
		database_client.update_db('INSERT INTO Submissions(username, submissionId, status) VALUES (?, ?, ?);', args=(self.username, self.submissionId, 'RUNNING'))
	
	def _handle_stdout(self):
		stdout, stderr = self._job.communicate()
		self._finalize()
		database_client.update_db('UPDATE Submissions SET stdout=?, stderr=? WHERE username=? AND submissionId=?;', args=(stdout, stderr, self.username, self.submissionId))
		database_client.update_db('UPDATE Submissions SET status=? WHERE username=? AND submissionId=? AND status=?;', args=('COMPLETED', self.username, self.submissionId, 'RUNNING'))
	
	def terminate(self):
		if _job.is_alive():
			database_client.update_db('UPDATE Submissions SET status=? WHERE username=? AND submissionId=?;', args=('TERMINATED', self.username, self.submissionId))
			self._job.terminate()
			return True
		else:
			return False
	
	def _finalize(self):		
		# Remove temp files
		os.remove(self._temp_conf_file_path)
		os.remove(self._temp_analyzer_script_path)
		os.rmdir(self._temp_directory)
 
