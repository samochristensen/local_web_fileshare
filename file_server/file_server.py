from flask import Flask, request, send_from_directory, send_file, render_template_string
import os
import zipfile
import io

app = Flask(__name__)
BASE_DIR = "C:/Users/SmartBeat/Documents/test_dir"  # Change this to your shared directory

@app.route('/')
def index():
    files = os.listdir(BASE_DIR)
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
        </style>
    </head>
    <body>
        <h1>Available Files</h1>
        <a href="/download-all" class="button">Download All as ZIP</a>
        <ul>
            {% for file in files %}
                <li><a href="/download/{{ file }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

@app.route('/download-all')
def download_all():
    # Create an in-memory ZIP file
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, BASE_DIR))
    memory_file.seek(0)
    
    # Send the zip file as a response
    return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='all_files.zip')

def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
