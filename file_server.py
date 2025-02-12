from flask import Flask, request, send_from_directory, render_template_string
import os

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
        </style>
    </head>
    <body>
        <h1>Available Files</h1>
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
