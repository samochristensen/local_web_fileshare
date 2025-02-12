# Local Web Fileshare

A simple Python-based file-sharing server with a web interface. It lets you browse files in a directory and download them individually or as a ZIP archive.

---

## Installation

1. **Clone the repository** (or navigate to your project directory):
    ```sh
    cd local_web_fileshare
    ```

2. **Set up a virtual environment** (recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the project as a package**:
    ```sh
    pip install .
    ```

---

## How to Run the File Server

After installing, you can run the server from anywhere with the command:
```sh
file-share
```

The server will start at `http://0.0.0.0:8080`. Open it in a browser to access the files.

### Features:
- **Download individual files** by clicking their name.
- **Download all files as a ZIP** using the "Download All as ZIP" button.

---

## Notes

- By default, it serves files from `C:/Users/SmartBeat/Documents/test_dir`. You can modify the directory in `file_server/server.py` (`BASE_DIR` variable).  
- This server is for local and private networks. For production, use a proper WSGI server like Gunicorn.

---

## Uninstall
If you ever want to remove it:
```sh
pip uninstall local-web-fileshare
```

