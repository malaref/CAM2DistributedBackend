from flask_api import app

from flask import flash, request, redirect, render_template

@app.route('/submit/', methods=['GET', 'POST'])
def submit():
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
 
