from flask import Flask, render_template
from flask_rbac import RBAC
from models import db, Role, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
rbac = RBAC(app)

with app.app_context():
    db.create_all()  # Crea las tablas en la base de datos

@rbac.set_role_model
class Role(db.Model, RoleMixin):
    # Código del modelo de rol

@rbac.set_user_model
class User(db.Model, UserMixin):
    # Código del modelo de usuario

@app.route('/')
def index():
    return "Home Page"

@app.route('/admin')
@rbac.allow(['admin'], methods=['GET'])
def admin_dashboard():
    return "Admin Dashboard"

@app.route('/user')
@rbac.allow(['user'], methods=['GET'])
def user_dashboard():
    return "User Dashboard"

if __name__ == '__main__':
    app.run(debug=True)
