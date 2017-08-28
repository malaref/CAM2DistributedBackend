from flask import Flask, flash, request, redirect, url_for, render_template, send_file, g
from clients.storage_client import StorageClient
from clients.database_client import DatabaseClient
from collections import deque
import atexit

app = Flask(__name__)
app.secret_key = 'some_secret'
master_url = 'spark://Exs:7077'
namenode_url = 'http://localhost:50070'
jobs = deque()
storage_client = StorageClient(namenode_url)
database_client = DatabaseClient('database.db')
atexit.register(database_client.close_connection)

import html_api
import json_api
