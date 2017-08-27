from flask_api import app, jobs, database_client

from flask import request,  jsonify
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
		jobs.append(JobClient(request.authorization.username, json.load(conf), analyzer_script))
		return 'Success!'
	return 'This is a GET'

@app.route('/json/status/')
@requires_auth
def json_status():
	submission_id = str(request.get_json()['submission_id'])
	return jsonify(database_client.query_db('SELECT * FROM Submissions WHERE submission_id=?', args=(submission_id,), one=True))
