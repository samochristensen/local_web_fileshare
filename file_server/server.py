from flask import Flask, send_from_directory, send_file, render_template_string, url_for
import os
import zipfile
import tempfile
import atexit

app = Flask(__name__)
BASE_DIR = os.getcwd()
temp_dir = tempfile.TemporaryDirectory()
ZIP_FILE_PATH = os.path.join(temp_dir.name, "all_files.zip")
zip_file_size = 0

def create_zip_file():
    global zip_file_size
    with zipfile.ZipFile(ZIP_FILE_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, BASE_DIR))
    zip_file_size = os.path.getsize(ZIP_FILE_PATH)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def index(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)

    if not os.path.exists(abs_path):
        return "<h1>404: Directory not found</h1>", 404

    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=True)

    files = os.listdir(abs_path)
    files = sorted(files, key=lambda x: (os.path.isdir(os.path.join(abs_path, x)), x.lower()))  # Sort directories first

    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 5px 0; }
            a { text-decoration: none; color: #1a73e8; }
            a:hover { text-decoration: underline; }
            .button { display: inline-block; padding: 10px 20px; color: white; background-color: #007BFF; text-decoration: none; border-radius: 5px; }
            .button:hover { background-color: #0056b3; }
            .path { font-size: 0.9em; color: #555; }
        </style>
    </head>
    <body>
        <h2 class="path">Shared Directory on Host Machine: {{ current_dir }}</h2>
        <a href="/download-all" class="button">Download Directory ({{ zip_size }})</a>
        <h2>Download individual files:</h2>
        <ul>
            {% if parent_dir %}
                <li><a href="{{ url_for('index', req_path=parent_dir) }}">..</a></li>
            {% endif %}
            {% for file in files %}
                <li>
                    {% if os.path.isdir(os.path.join(current_dir, file)) %}
                        <a href="{{ url_for('index', req_path=req_path + '/' + file if req_path else file) }}">{{ file }}/</a>
                    {% else %}
                        <a href="{{ url_for('index', req_path=req_path + '/' + file if req_path else file) }}">{{ file }}</a>
                    {% endif %}
                </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    parent_dir = os.path.dirname(req_path) if req_path else None
    zip_size = format_size(zip_file_size)
    return render_template_string(template, files=files, req_path=req_path, current_dir=abs_path, parent_dir=parent_dir, zip_size=zip_size, os=os)

@app.route('/download-all')
def download_all():
    return send_file(ZIP_FILE_PATH, mimetype='application/zip', as_attachment=True, download_name='all_files.zip')

def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def main():
    global BASE_DIR
    BASE_DIR = os.getcwd()
    print(f"Serving files from: {BASE_DIR}")
    print("Creating zip file...")
    create_zip_file()
    print(f"Zip file created: {ZIP_FILE_PATH} ({format_size(zip_file_size)})")

    atexit.register(temp_dir.cleanup)
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
