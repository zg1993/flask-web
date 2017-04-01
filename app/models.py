#!/usr/bin/env python
#-*- coding: utf-8-*-

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app 
from . import login_manager


class Role(db.Model):


	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')
	def __repr__(self):
		return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique = True)
	#password = db.Column(db.string(64))
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	confirmed = db.Column(db.Boolean, default=False)


	def __repr__(self):
		return '<User {}>'.format(self.username)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password) 

	def generate_confirmation_token(self, expiration=180):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			print('except')
			return False
		if data.get('confirm') != self.id:
			print('self.id:{}'.format(self.id))
			return False
		self.confirmed = True
		db.session.add(self)
		return True

@login_manager.user_loader
def load_user(user_id):
	print('into...load_user{}'.format(user_id))
	return User.query.get(int(user_id))

