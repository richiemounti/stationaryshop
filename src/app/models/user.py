import sys
from app.extensions import db
from datetime import datetime, timedelta
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from app.extensions import bcrypt, login
import jwt
import sys
import json

class Permission:
    GENERAL = 0
    ADMINISTER = 1

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    role_id = db.Column(db.Integer)


    def __init__(self, username, email, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        print('hiii', sys.stdout)
        print(email, sys.stdout)
        print(current_app.config['ADMIN_EMAIL'], sys.stdout)
        print(self.role_id, sys.stdout)
        if self.role_id is None:
            if email == current_app.config['ADMIN_EMAIL']:
                self.role_id = 1
                print(self.role_id, sys.stdout)
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def can(self, permissions):
            return self.role_id is not None and \
                (self.role_id.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
