#!/usr/bin/env python
#-*- coding: utf-8-*-

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app 
from . import login_manager
from datetime import datetime
import hashlib
from flask import request


class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80


#article model
class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')


	def __repr__(self):
		return '<Role {}>'.format(self.name)

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.FOLLOW |
					 Permission.COMMENT |
					 Permission.WRITE_ARTICLES, True),
			'Moderator': (Permission.FOLLOW |
						  Permission.COMMENT |
						  Permission.WRITE_ARTICLES |
						  Permission.MODERATE_COMMENTS, False),
			'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique = True)
	#password = db.Column(db.string(64))
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	confirmed = db.Column(db.Boolean, default=False)
	#add other info
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since =db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	#add avatar_hash
	avatar_hash = db.Column(db.String(32))
	#add article
	posts = db.relationship('Post', backref='au', lazy='dynamic')


	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.email is not None and self.avatar_hash is None:
			self.avatar_hash = hashlib.md5(
				self.email.encode('utf-8')).hexdigest()
		print('into...User__init__')
		if self.role is None:
			if self.email == current_app.config['FLASKY_ADMIN']:
				print('__init__create admin {}'.format(current_app.config['FLASKY_ADMIN']))
				self.role = Role.query.filter_by(permissions=0xff).first()
				print('self.role:{}'.format(self.role))
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()

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

	def can(self, permissions):
		print('into can.....', self.role.permissions, permissions)
		return self.role is not None and \
				(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)

	#update last_time
	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	#gravatar
	# def change_email(self, token):
	# 	self.email = new_email
	# 	self.avatar_hash = hashlib.md5(
	# 		self.email.encode('utf-8')).hexdigest()
	# 	db.session.add(self)
	# 	return True

	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://s.gravatar.com/avatar'
		hash = self.avatar_hash or hashlib.md5(
			self.email.encode('utf-8')).hexdigest()
		print('into..gravatar..{url}/{hash}?s={size}&d={default}&r={rating}'.format(
			url=url, hash=hash, size=size, default=default, rating=rating))
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
			url=url, hash=hash, size=size, default=default, rating=rating)


class AnonymousUser(AnonymousUserMixin):


	def can(self, permissions):
		return False

	def is_administrator(self):
		return False


@login_manager.user_loader
def load_user(user_id):
	print('into...load_user{}'.format(user_id))
	return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser

