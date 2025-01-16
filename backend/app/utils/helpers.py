import uuid
from datetime import datetime
from flask_uploads import UploadSet, configure_uploads, ALL
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Define the UploadSet for file uploads
files = UploadSet(name='files', extensions=ALL)

def init_file_uploads(app):
    app.config['UPLOADED_FILES_DEST'] = 'static/uploads'
    configure_uploads(app, files)

def generate_unique_id():
    return str(uuid.uuid4())

def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if isinstance(dt, datetime) else None

def paginate_query(query, page, per_page):
    return query.paginate(page=page, per_page=per_page, error_out=False)

# Example of secure_filename usage for additional file handling
def save_file(file):
    """Save the uploaded file securely."""
    filename = secure_filename(file.filename)
    file_path = f"static/uploads/{filename}"
    file.save(file_path)
    return file_path