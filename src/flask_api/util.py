import subprocess, tempfile, os, json, shutil

def submit_to_spark(conf, analyzer_script):
	# Create temp files
	temp_directory = tempfile.mkdtemp()
	temp_conf_file_path = os.path.join(temp_directory, 'user_conf.json')
	temp_analyzer_script_path = os.path.join(temp_directory, 'user_analyzer.py')
	with open(temp_conf_file_path, 'w') as f:
		json.dump(conf, f, sort_keys=True, indent=4)
	analyzer_script.save(temp_analyzer_script_path)
	
	# Submit to Spark
	subprocess.call('$SPARK_HOME/bin/spark-submit --py-files core/cam2.zip,{1} core/main.py {0}'.format(temp_conf_file_path, temp_analyzer_script_path), shell=True)
	
	# Remove temp files
	os.remove(temp_conf_file_path)
	os.remove(temp_analyzer_script_path)
	os.rmdir(temp_directory)
 
def prepare_result(username, submission_id, namenode_ip='localhost', namenode_port='50070'):
	from hdfs import InsecureClient # TODO DRYing the HDFS client
	client = InsecureClient('http://{0}:{1}'.format(namenode_ip, namenode_port))
	temp_directory = tempfile.mkdtemp() # TODO DRYing this pattern
	client.download('/'.join(['/users', username, str(submission_id)]), temp_directory)
	archive_name = shutil.make_archive(str(submission_id), 'zip', temp_directory)
	shutil.rmtree(temp_directory)
	return archive_name
