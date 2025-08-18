# from flask_limiter      import Limiter
# from flask_limiter.util import get_remote_address
from app                import app
from flask_login        import LoginManager, current_user
from flask_mail         import Mail

# limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()
mail = Mail()