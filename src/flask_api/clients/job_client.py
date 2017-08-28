from flask_api import jobs, database_client, master_url, namenode_url

import tempfile, os, json, subprocess, threading

class JobClient(object):
	
	@classmethod
	def submit_job(cls, username, json_conf, analyzer_script):
		jobs.append(cls(username, json_conf, analyzer_script))
	
	@classmethod
	def terminate_job(cls, username, submission_id):
		for job in jobs:
			if job.username == username and job.submission_id == submission_id:
				return job.terminate()
		return False
	
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
		self.submission_id = conf['submission_id']
		# Submit the job
		self._job = subprocess.Popen('exec $SPARK_HOME/bin/spark-submit --py-files core/cam2.zip,{4} core/main.py {0} {1} {2} {3}'.format(master_url, namenode_url, self.username, self._temp_conf_file_path, self._temp_analyzer_script_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		threading.Thread(target=self._handle_stdout).start()
		database_client.update_db('INSERT INTO Submissions(username, submission_id, status, stdout, stderr) VALUES (?, ?, ?, ?, ?);', args=(self.username, self.submission_id, 'RUNNING', 'Will be available upon completion/termination!', 'Will be available upon completion/termination!'))
	
	# TODO Make output available as it arrives
	def _handle_stdout(self):
		stdout, stderr = self._job.communicate()
		self._finalize()
		database_client.update_db('UPDATE Submissions SET stdout=?, stderr=? WHERE username=? AND submission_id=?;', args=(stdout, stderr, self.username, self.submission_id))
		database_client.update_db('UPDATE Submissions SET status=? WHERE username=? AND submission_id=? AND status=?;', args=('COMPLETED', self.username, self.submission_id, 'RUNNING'))
		jobs.remove(self)
	
	def terminate(self):
		if self._job.poll() is None:
			database_client.update_db('UPDATE Submissions SET status=? WHERE username=? AND submission_id=?;', args=('TERMINATED', self.username, self.submission_id))
			self._job.terminate()
			return True
		else:
			return False
	
	def _finalize(self):		
		# Remove temp files
		os.remove(self._temp_conf_file_path)
		os.remove(self._temp_analyzer_script_path)
		os.rmdir(self._temp_directory)
