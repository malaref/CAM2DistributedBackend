from flask import Flask, flash, request, redirect, url_for, render_template
import subprocess

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            file.save('tmp/user_analyzer.py')
            subprocess.call("$SPARK_HOME/bin/spark-submit --master local[3] --py-files core/cam2.zip,tmp/user_analyzer.py core/main.py", shell=True)
            flash('Done!')
        return redirect(request.url)
    return render_template('submit.html')
