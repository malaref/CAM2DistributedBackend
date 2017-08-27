from flask import Flask, flash, request, redirect, url_for, render_template, send_file, g
from clients.storage_client import StorageClient

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/<username>/<int:submission_id>/')
def get_result(username, submission_id):
	return send_file(StorageClient.prepare_result_as_zip_file(username, submission_id)) # TODO Better way to ensure disposal of the file

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

import html_api
import json_api
