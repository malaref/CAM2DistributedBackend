from flask_api import app

from flask import request
from clients.authentication_client import requires_auth
from clients.job_client import JobClient

import json

@app.route('/json/submit/', methods=['GET', 'POST'])
@requires_auth
def json_submit():
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
		# TODO Better control
		job_client = JobClient(json.load(conf), analyzer_script)
		job_client.submit()
		job_client.finalize()
		return 'Success!'
	return 'This is a GET'
