import os
import csv
import cv2
import random
from app import app
from adddb import database
from encode import imgUpload
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file(): 
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			name = request.form.get('name')
			std = request.form.get('class')
			# ids = request.form.get('id')
			ids = ''.join(str(random.randint(0,9)) for x in range(6))
			fieldnames = ['Name', 'Class', 'ID']
			with open('students.csv','a') as inFile:
				writer = csv.DictWriter(inFile, fieldnames=fieldnames)
				writer.writerow({'Name': name, 'Class': std, 'ID':ids})
			
			data = {
       				ids:
					{
						"name": name,
						"total_attendance": 0,
						"standard": std,
						"last_attendance_time": "2023-05-23 08:05:05"
					}
     			   }
			print('Data:::\n', data)
			database(data)

			print('filename:', file.filename.split('.')[0])
			stuid = file.filename.split('.')[0].replace(file.filename.split('.')[0], ids)
			path = str(stuid)+'.jpg'         # '.' +file.filename.split('.')[1]
			print('path:', path)

			imgpath = secure_filename(path)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], imgpath))
			flash('File successfully uploaded')

			imgUpload(path)
			return redirect('/')

		else:
			flash('Allowed file types are png, jpg, jpeg')
			return redirect(request.url)

		if request.method == 'GET':
			return render_template('upload.html')

if __name__ == "__main__":
    app.run()
