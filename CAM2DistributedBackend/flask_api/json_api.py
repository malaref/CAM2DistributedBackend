from CAM2DistributedBackend.flask_api import app, database_client, storage_client

from flask import request,  jsonify, send_file, after_this_request
from clients.authentication_client import requires_auth
from clients.job_client import JobClient

import json, os

# NOTE May move this method to the DatabaseClient class
def _get_submission(username, submission_id):
	return database_client.query_db('SELECT * FROM Submissions WHERE username=? AND submission_id=?', args=(username, submission_id), one=True)

@app.route('/json/submit/', methods=['POST'])
@requires_auth
def json_submit():
	username = request.authorization.username
	if not request.files.has_key('conf'):
		return 'No configuration file'
	elif not request.files.has_key('analyzer'):
		return 'No analyzer script'
	conf = request.files['conf']
	analyzer = request.files['analyzer']
	if conf.filename == '':
		return 'No selected configuration file'
	elif analyzer.filename == '':
		return 'No selected analyzer script'
	elif not conf.filename.endswith('.json'):
		return 'The configuration file must be a JSON file'
	elif not analyzer.filename.endswith('.py'):
		return 'The analyzer script must be a Python script'
	json_conf = json.load(conf)
	if _get_submission(username, json_conf['submission_id']) is not None:
		return 'Cannot have two submissions with the same "submission_id"'
	JobClient.submit_job(username, json_conf, analyzer)
	return 'Job submitted!'

@app.route('/json/status/', methods=['POST'])
@requires_auth
def json_status():
	username = request.authorization.username
	submission_id = request.get_json()['submission_id']
	submission = _get_submission(username, submission_id)
	not_found = 'Could not find a submission with "submission_id" = {}'.format(submission_id)
	
	if submission is None:
		return not_found
	return jsonify(submission)

@app.route('/json/terminate/', methods=[ 'POST'])
@requires_auth
def json_terminate():
	username = request.authorization.username
	submission_id = request.get_json()['submission_id']
	submission = _get_submission(username, submission_id)
	terminated = 'Submission with "submission_id" = {} terminated!'.format(submission_id)
	not_running = 'Submission with "submission_id" = {} is not running!'.format(submission_id)
	not_found = 'Could not find a submission with "submission_id" = {}'.format(submission_id)
	
	if submission is None:
		return not_found
	if submission['status'] == 'RUNNING' and JobClient.terminate_job(username, submission_id):
		return terminated
	return not_running

@app.route('/json/download/', methods=[ 'POST'])
@requires_auth
def json_download():
	username = request.authorization.username
	submission_id = request.get_json()['submission_id']
	submission = _get_submission(username, submission_id)
	not_found = 'Could not find a submission with "submission_id" = {}'.format(submission_id)
	running = 'Submission with "submission_id" = {} is running!'.format(submission_id)
	
	if submission is None:
		return not_found
	elif submission['status'] == 'RUNNING':
		return running
	file_name = storage_client.prepare_result_as_zip_file(username, submission_id)
	
	@after_this_request
	def remove_file(response):
		os.remove(file_name)
		return response
	return send_file(file_name)

@app.route('/json/delete/', methods=[ 'POST'])
@requires_auth
def json_delete():
	username = request.authorization.username
	submission_id = request.get_json()['submission_id']
	submission = _get_submission(username, submission_id)
	not_found = 'Could not find a submission with "submission_id" = {}'.format(submission_id)
	running = 'Submission with "submission_id" = {} is running!'.format(submission_id)
	deleted = 'Submission with "submission_id" = {} deleted!'.format(submission_id)
	
	if submission is None:
		return not_found
	elif submission['status'] == 'RUNNING':
		return running
	
	database_client.update_db('DELETE FROM Submissions WHERE submission_id=?', args=(submission_id,))
	storage_client.delete_result(username, submission_id)
	return deleted
