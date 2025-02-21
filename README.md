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
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
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

The server will start at `http://<your-ip-address>:8080`. Open it in a browser to access the files.

### Features:
- **Download individual files** by clicking their name.
- **Download all files as a ZIP** using the "Download All as ZIP" button.
- **Navigate directories** and return to the parent directory.

---

## Notes

- By default, it serves files from the current directory where the `file-share` command is executed.  
- This server is for local and private networks. For production, use a proper WSGI server like Gunicorn.

---

## PowerShell Execution Policy Issue

If you encounter an error saying that scripts cannot run, it may be due to PowerShell's execution policy.

### Solution:
1. **Check the current execution policy**:
    ```powershell
    Get-ExecutionPolicy
    ```
    If the output is `Restricted`, you'll need to change it.

2. **Temporarily allow scripts for the current session**:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```
    This change applies only to the current session and will not affect future sessions.

3. **Permanently allow scripts for the current user** (requires admin privileges):
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
    `RemoteSigned` is recommended for security.

Alternatively, you can run the server directly with Python:
```sh
python file_server/server.py
```

---

## Uninstall
If you ever want to remove it:
```sh
pip uninstall local-web-fileshare
```

