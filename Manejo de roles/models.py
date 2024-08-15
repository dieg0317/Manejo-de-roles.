from flask_sqlalchemy import SQLAlchemy
from flask_rbac import RoleMixin, UserMixin

db = SQLAlchemy()

roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    parents = db.relationship(
        'Role',
        secondary=roles_parents,
        primaryjoin=(id == roles_parents.c.role_id),
        secondaryjoin=(id == roles_parents.c.parent_id),
        backref=db.backref('children', lazy='dynamic')
    )

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    roles = db.relationship(
        'Role',
        secondary='users_roles',
        backref=db.backref('users', lazy='dynamic')
    )

    def add_role(self, role):
        self.roles.append(role)

    def get_roles(self):
        return self.roles
