import os
import time
from flask import current_app

def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set

def save_uploaded_file(file, folder, prefix=""):
    """
    Simpan file upload ke folder yang ditentukan.
    Return: nama file yang disimpan.
    """
    if not file or not file.filename:
        return None
    fname = f"{prefix}{int(time.time())}_{file.filename.replace(' ', '_')}"
    path = os.path.join(folder, fname)
    file.save(path)
    return fname