from sqla import sqla
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

class User(sqla.Model):
    __tablename__ = "users"

    id                 = sqla.Column(sqla.Integer(), primary_key=True)
    username           = sqla.Column(sqla.Text(), unique=True, nullable=False)
    email              = sqla.Column(sqla.String(64), unique=True, index=True, nullable=False)
    description        = sqla.Column(sqla.Text(), nullable=False)
    location           = sqla.Column(sqla.String(255), nullable=False)
    password_hash      = sqla.Column(sqla.Text(), nullable=False)

    def __init__(self, username="", email="", password="", location="", description=""):
        self.username         = username
        self.email            = email
        self.password_hash    = generate_password_hash(password)
        self.location         = location
        self.description      = description
    
    @validates('username', 'password')
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f'{key.capitalize()} is required.')
        
        if key == 'username':
            self.validate_unique(key, value, f'{value} already registered')

        if key == 'password':
            value = generate_password_hash(value)

        return value
        
    def validate_unique(self, key, value, error_message=None):
        if (
            User.query.filter_by(**{key: value}).first()
            is not None
        ):
            if not error_message:
                error_message = f'{key} must be unique.'
            raise ValueError(error_message)
        
        return value


    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError("Password should not be read like this")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)