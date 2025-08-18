from flask_login        import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app                import app, db
from app.extensions     import login_manager

login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    c = db.koneksi_database()
    cursor = c.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_login WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    c.close()
    if user:
        return User(id=user['id'], username=user['username'], password=user['password'])
    return None