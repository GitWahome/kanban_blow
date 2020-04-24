from kanban import db, login_manager
from flask_login import UserMixin


locals()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Todos Model
class Todos(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    todo_item = db.Column(db.String(500),  nullable=True)
    todo_date = db.Column(db.String(500), nullable=True)
    todo_status = db.Column(db.String(10), nullable=False, default='todo')
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(500), db.ForeignKey('user.email'), nullable=True)
    def __repr__(self):
        return f'Todo item {self.todo_item} due on {self.todo_date}'



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todos', cascade='all, delete-orphan', backref='author', lazy=True)