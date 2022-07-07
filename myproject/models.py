from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True)
    registration_number = db.Column(db.String(64), unique=True, index=True)
    Role = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, registration_number, Role,password ):
        self.email = email
        self.username = username
        self.registration_number = registration_number
        self.Role = Role

        self.password_hash = generate_password_hash(password)
    def __str__(self):
        return f"{self.email, self.username,self.registration_number, self.Role } "

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)
