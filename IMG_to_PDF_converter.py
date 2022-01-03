import os
from flask import Flask, render_template, request
from PIL import Image
from flask import Flask, render_template, request, flash
from flask.helpers import send_file
from werkzeug.utils import redirect, secure_filename
from werkzeug.datastructures import MultiDict

app = Flask(__name__)


def converter(images):
    imagelist = []
    if(len(images)==1):
        Image.open(images[0]).convert('RGB').save('PJImageConveter.pdf')
        return
    for img in images[1:]:
        imagelist.append(Image.open(img).convert('RGB'))

    Image.open(images[0]).convert('RGB').save('PJImageConveter.pdf', save_all=True,
                    append_images=imagelist)


ALLOWED_EXTENSION = set(['png', 'jpg', 'jpeg', 'gif'])


def allowedFile(filename):
    return "." in filename and filename.rsplit(".", 1)[0].lower in ALLOWED_EXTENSION


app = Flask(__name__)


@app.route('/')
def upload_file1():
    return render_template('index.html')

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(file):
    return file.split(".")[1] in ALLOWED_EXTENSIONS
    
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        toConveredList=[]
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return 'No file part'
        
        file = request.files['file']

        if file.filename == '':
            # flash('No selected file')
            return 'No selected file'
            
        imgList=MultiDict(request.files).getlist('file')
        for i in imgList:
            if i and allowed_file(i.filename):
                filename = secure_filename(file.filename)
                i.save(filename)
                toConveredList.append(filename)
        converter(toConveredList)
        return send_file('PJImageConveter.pdf', as_attachment=True)

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(filename)
            converter([filename])
            return send_file('PJImageConveter.pdf', as_attachment=True)
            return "<script>alert('converted')</script>"

@app.route('/download')
def download():
    return send_file('PJImageConveter.pdf')

if __name__ == '__main__':
    app.run(debug=True)
