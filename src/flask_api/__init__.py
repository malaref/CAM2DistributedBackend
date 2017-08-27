from flask import Flask, flash, request, redirect, url_for, render_template, send_file, g
from clients.storage_client import StorageClient
from clients.database_client import DatabaseClient
from collections import deque
import atexit

app = Flask(__name__)
app.secret_key = 'some_secret'
jobs = deque()
database_client = DatabaseClient('database.db')
atexit.register(database_client.close_connection)

@app.route('/<username>/<int:submission_id>/')
def get_result(username, submission_id):
	return send_file(StorageClient.prepare_result_as_zip_file(username, submission_id)) # TODO Better way to ensure disposal of the file

import html_api
import json_api
