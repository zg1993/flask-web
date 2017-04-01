#!/usr/bin/env python
#-*- coding: utf-8-*-


from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_user


@main.route('/', methods=['GET', 'POST'])
def index():
	print('index')
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		user = User.query.filter_by(username=name).first()
		if user is None:
			print('user: %s'%user)
			user = User(username=name)
			print(db)
			db.session.add(user)
			#db.session.commit()
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = name
		return redirect(url_for('.index'))
	return render_template('index.html', 
							form=form, name=session.get('name'),
							known=session.get('known', False),
							current_time=datetime.utcnow())

@main.route('/home')
def home():
	#print('current_user:{}'.format(current_user))
	return render_template('home.html')


