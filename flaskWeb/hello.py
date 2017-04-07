#!/usr/bin/env python
#-*- coding: utf-8-*-

from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask.ext.script import Manager
from flask import render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import url_for
from flask import session
from flask import flash
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail


#form class
class NameForm(Form):
	name = StringField('what is your name', validators=[Required()])
	submit = SubmitField('Submit')


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
app.config['SECRET_KEY'] = 'sheng ming'
bootstrap = Bootstrap(app)
manager = Manager(app)

#see OMail
#app.config['MAIL_SERVER'] = 'smtp.alimail.com'
app.config['MAIL_SERVER'] = 'smtp.kiyozawa.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)
#sql model
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role {}>'.format(self.name)


user_article = db.Table('user_article', 
	db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
	db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True)
	)


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	articles = db.relationship('Article', secondary=user_article, backref=db.backref('users', lazy='dynamic'))

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), unique=True, index=True)
	#author = db.Column(db.String(64), db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<Article {}>'.format(self.title)




def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Article=Article)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	name = None
	if form.validate_on_submit():
		name = form.name.data
		session['name'] = name
		return redirect(url_for('index'))
	#form.name.data = ''
	return render_template('index1.html', form=form, name=session.get('name'))
	#name = None
	# form = NameForm()
	# if form.validate_on_submit():
	# 	user = User.query.filter_by(username=form.name.data).first()
	# 	print('user: ', user)
	# 	if user is None:
	# 		user = User(username=form.name.data, role_id=3)
	# 		db.session.add(user)
	# 		session['known'] = False
	# 	else:
	# 		session['known'] = True
	# 	old_name = session.get('name')
	# 	if old_name is not None and old_name != form.name.data:
	# 		flash('you have changed your name')
	# 	print('submit name: {}'.format(form.name.data))
	# 	session['name'] = form.name.data
	# 	form.name.data = ''
	# 	return redirect(url_for('index'))
	# 	#name = form.name.data
	# 	#form.name.data = ''
	# return render_template('index.html', form = form, name=session.get('name'), known=session.get('known'))
	#response = make_response('<h1>This document carries a cookie!</h1>')
	#response.set_cookie('answer', '42')
	#abort(404)
	#return render_template('index.html')
	#return response
	#return redirect('http://www.baidu.com')
	# user_agent = request.headers.get('User-Agent')
	# return '<h1>user_t: {}</h1>'.format(user_agent)
	#return ('bad', 404)
	#return render_template('index.html', form=form, name=name)


@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		session['name'] = form.name.data
		if old_name is not None and old_name != form.name.data:
			flash('you have changed your name')
		return redirect(url_for('user', name=name, _external=True))
	print(session.get('name'))
	return render_template('user.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
	#return render_template('user.html', form=form, name=name)
	#return render_template('index.html', form = form, name=session.get('name'))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500'), 500


if __name__ == '__main__':
	#app.run(debug=True)
	app.debug=True
	manager.run()
	#bootstrap.run()