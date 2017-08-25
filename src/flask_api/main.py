from flask import Flask, flash, request, redirect, url_for, render_template
import subprocess, tempfile, os, json

app = Flask(__name__)
app.secret_key = 'some_secret'

def submit_to_spark(conf, analyzer_script):
	# Create temp files
	temp_directory = tempfile.mkdtemp()
	temp_conf_file_path = os.path.join(temp_directory, 'user_conf.json')
	temp_analyzer_script_path = os.path.join(temp_directory, 'user_analyzer.py')
	with open(temp_conf_file_path, 'w') as f:
		json.dump(conf, f, sort_keys=True, indent=4)
	analyzer_script.save(temp_analyzer_script_path)
	
	# Submit to Spark
	subprocess.call("$SPARK_HOME/bin/spark-submit --master local[3] --py-files core/cam2.zip,{1} core/main.py {0}".format(temp_conf_file_path, temp_analyzer_script_path), shell=True)
	
	# Remove temp files
	os.remove(temp_conf_file_path)
	os.remove(temp_analyzer_script_path)
	os.rmdir(temp_directory)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'analyzer_script' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['analyzer_script']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		elif not file.filename.endswith('.py'):
			flash('The selected file must be a Python script')
		else:
			temp_directory = tempfile.mkdtemp()
			temp_file = os.path.join(temp_directory, 'user_analyzer.py')
			file.save(temp_file)
			subprocess.call("$SPARK_HOME/bin/spark-submit --master local[3] --py-files core/cam2.zip,{} core/main.py".format(temp_file), shell=True)
			os.remove(temp_file)
			os.rmdir(temp_directory)
			flash('Done!')
		return redirect(request.url)
	return render_template('submit.html')

@app.route('/json/', methods=['GET', 'POST'])
def json_api():
	if request.method == 'POST':
		if not request.files.has_key('conf'):
			return 'No configuration file'
		elif not request.files.has_key('analyzer_script'):
			return 'No analyzer script'
		conf = request.files['conf']
		analyzer_script = request.files['analyzer_script']
		if conf.filename == '':
			return 'No selected configuration file'
		elif analyzer_script.filename == '':
			return 'No selected analyzer script'
		elif not conf.filename.endswith('.json'):
			return 'The configuration file must be a JSON file'
		elif not analyzer_script.filename.endswith('.py'):
			return 'The analyzer script must be a Python script'
		submit_to_spark(json.load(conf), analyzer_script)
		return 'Success!'
	return 'This is a GET'

