import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import evaluate
UPLOAD_FOLDER = os.getcwd()+'/examples'


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/up/<path:filename>')
def download_file(filename):
    print(filename)
    return send_from_directory((app.config['UPLOAD_FOLDER']+'/thumbs/'),
                               filename, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            evaluate.ins=UPLOAD_FOLDER+'/'+filename
            evaluate.outs=os.getcwd()+'/examples/thumbs/'+filename
            evaluate.main()
            return send_from_directory((app.config['UPLOAD_FOLDER']+'/thumbs/'),
                               filename, as_attachment=True)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
app.run(debug = True)