from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Create users table"""

    __tablename__ = "users"
    
    username = db.Column(db.String(20), 
                         unique=True, 
                         nullable=False, 
                         primary_key=True)
    password = db.Column(db.Text, 
                         nullable=False)
    email = db.Column(db.String(50), 
                      nullable=False, 
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30), 
                          nullable=False)
    is_admin = db.Column(db.Boolean,
                         nullable=False,
                         default=False)
    
    feedback = db.relationship('Feedback', cascade="all, delete", backref='user')
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name, is_admin=False):
        """Register user with hashed password"""


        hashed = bcrypt.generate_password_hash(password)
        #turn into normal string to store
        hashed_ut8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_ut8, email=email, first_name=first_name, last_name=last_name, is_admin=is_admin)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct.
        
        Return user if valid.
        Return false if user not valid.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    """Feedback table"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String, 
                         db.ForeignKey('users.username'),
                         nullable=False)