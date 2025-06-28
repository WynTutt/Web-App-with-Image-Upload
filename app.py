from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_IP = '20.218.226.24'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


#@app.before_request
#def limit_remote_addr():
#    if request.remote_addr != ALLOWED_IP:
#        abort(403)

@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
