import subprocess, tempfile, os, json

class JobClient(object):
	
	def __init__(self, conf, analyzer_script):
		# Create temp files
		self.temp_directory = tempfile.mkdtemp()
		self.temp_conf_file_path = os.path.join(self.temp_directory, 'user_conf.json')
		self.temp_analyzer_script_path = os.path.join(self.temp_directory, 'user_analyzer.py')
		with open(self.temp_conf_file_path, 'w') as f:
			json.dump(conf, f, sort_keys=True, indent=4)
		analyzer_script.save(self.temp_analyzer_script_path)
	
	def submit(self):
		subprocess.call('$SPARK_HOME/bin/spark-submit --py-files core/cam2.zip,{1} core/main.py {0}'.format(self.temp_conf_file_path, self.temp_analyzer_script_path), shell=True)
	
	def finalize(self):		
		# Remove temp files
		os.remove(self.temp_conf_file_path)
		os.remove(self.temp_analyzer_script_path)
		os.rmdir(self.temp_directory)
 
