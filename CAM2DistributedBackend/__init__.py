from flask import Flask, flash, request, redirect, url_for, render_template, send_file, g
from clients.storage_client import StorageClient
from clients.database_client import DatabaseClient
from collections import deque
import os, json, sqlite3, atexit

app = Flask(__name__)
app.secret_key = 'some_secret'
resource_path = os.path.join(app.root_path, 'resources')

# Cache
cache_path = os.path.join(os.path.expanduser('~'), '.CAM2DistributedBackend')
if not os.path.exists(cache_path):
	os.makedirs(cache_path)

# Configuration
config_path = os.path.join(cache_path, 'config.json')
if not os.path.exists(config_path):
	master_url = raw_input('Spark master URL: ')
	namenode_url = raw_input('HDFS namenode URL: ')
	with open(config_path, 'w') as f:
		config = json.dump({'master_url': master_url, 'namenode_url':namenode_url}, f)
else:
	with open(config_path, 'r') as f:
		config = json.load(f)
	master_url = config['master_url']
	namenode_url = config['namenode_url']

# Database
database_path = os.path.join(cache_path, 'database.db')
if not os.path.exists(database_path):
	with open(os.path.join(resource_path, 'db.sql')) as schema:
		conn = sqlite3.connect(database_path)
		conn.executescript(schema.read())
		conn.commit()
		conn.close()

jobs = deque()
storage_client = StorageClient(namenode_url)
database_client = DatabaseClient(database_path)
atexit.register(database_client.close_connection)

import routes
