from flask import Flask, send_from_directory, send_file, render_template_string
import os
import zipfile
import io

app = Flask(__name__)
BASE_DIR = os.getcwd()

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def index(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)

    if not os.path.exists(abs_path):
        return "<h1>404: Directory not found</h1>", 404

    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=True)

    files = os.listdir(abs_path)
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
        <h1>File Server</h1>
        <p class="path">Current Directory: {{ current_dir }}</p>
        <a href="/download-all" class="button">Download Directory -- Zipped </a>
    </body>
    </html>
    '''
    parent_dir = os.path.dirname(req_path) if req_path else None
    return render_template_string(template, files=files, req_path=req_path, current_dir=abs_path, parent_dir=parent_dir)

@app.route('/download-all')
def download_all():
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, BASE_DIR))
    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='all_files.zip')

def main():
    global BASE_DIR
    BASE_DIR = os.getcwd()
    print(f"Serving files from: {BASE_DIR}")
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
