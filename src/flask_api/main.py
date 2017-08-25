from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from util import submit_to_spark, prepare_result
import json

app = Flask(__name__)
app.secret_key = 'some_secret'

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

@app.route('/<username>/<int:submission_id>/')
def get_result(username, submission_id):
	return send_file(prepare_result(username, submission_id)) # TODO Better way to ensure disposal of the file
