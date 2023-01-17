from flask import Flask,render_template,request,redirect,url_for,abort,send_from_directory
from werkzeug.utils import secure_filename # helps to convert bad file name into a secure filename
import os
app=Flask(__name__)
app.config['max_CONTENT_LENGTH'] = 1024 * 1024 *2
app.config['UPLOAD_EXTENSIONS'] = ['.jpg','.png','.gif','.jpeg']
app.config['UPLOAD_PATH']='uploads'


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('upload.html',upfiles=files)

@app.route('/',methods=['POST'])
def upload_file():
    uploaded_file=request.files.get('file')   #we getting the file from form
    filename = secure_filename(uploaded_file.filename) #clean the file name and store the varriable 
    if filename != '':  # if the filename is not empty
        file_ext = os.path.splitext(filename)[1] #get the extension from the file name ex. abc.png['abc', 'png']
        if file_ext not in app.config['UPLOAD_EXTENSIONS']: # if extension is not valid 
            abort(400)                                       # then stop the execution else
        path=os.path.join(app.config['UPLOAD_PATH'],filename)   # make os compatible   path string
        uploaded_file.save(path) # then save the file with original name 
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],filename) 
@app.errorhandler(413)
def too_large(e):
    return "file is too large",413

if __name__ == '__main__':
    app.run(debug=True)