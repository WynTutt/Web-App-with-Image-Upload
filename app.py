from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_IP = '20.218.226.24'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.before_request
def limit_remote_addr():
    if request.remote_addr != ALLOWED_IP:
        abort(403)

# Helper function to validate and sanitize filenames
def is_safe_path(base_path, user_input):
    # Normalize the full path and check it stays inside the allowed directory
    target_path = os.path.abspath(os.path.join(base_path, user_input))
    return target_path.startswith(os.path.abspath(base_path))

@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        filename = file.filename
        if not is_safe_path(UPLOAD_FOLDER, filename):
            abort(400, "Invalid filename.")
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if not is_safe_path(UPLOAD_FOLDER, filename):
        abort(400, "Invalid filename.")
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if not is_safe_path(UPLOAD_FOLDER, filename):
        abort(400, "Invalid filename.")
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
