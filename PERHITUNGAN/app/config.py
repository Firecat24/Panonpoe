import os

from dotenv             import load_dotenv
from app                import app
from datetime           import timedelta
from itsdangerous       import URLSafeTimedSerializer
from app.extensions     import mail, login_manager

load_dotenv()
mail.init_app(app)
# limiter.init_app(app)
login_manager.init_app(app)

app.secret_key = os.getenv('SECRET_KEY_FLASK')

keamanan_token = URLSafeTimedSerializer('SECRET_KEY_TOKEN')

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=3)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'gambar_upload')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Path ke file
posisi_matahari = os.path.join("app", "static", "files", "posisi_matahari.txt")
posisi_bulan = os.path.join("app", "static", "files", "posisi_bulan.txt")
posisi_hilal = os.path.join("app", "static", "files", "posisi_hilal.txt")
fase_bulan = os.path.join("app", "static", "files", "fase_bulan.txt")