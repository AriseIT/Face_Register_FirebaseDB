from flask import Flask
import os

try:
    os.mkdir('Images')
except OSError as e:
    pass
UPLOAD_FOLDER = 'Images'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

