#!/usr/bin/env python
#-*- coding: utf-8-*-


from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm 
from .. import db
from ..models import User, Permission, Role, Post
from flask_login import login_user, login_required
from ..decorators import admin_required, permission_required
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
	print('index')
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data, au=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html', form=form, posts=posts)

@main.route('/home')
def home():
	#print('current_user:{}'.format(current_user))
	return render_template('home.html')


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
	return "For administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return 'For comment moderators!'	


#user info
@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	users = User.query.order_by(User.username).all()
	if user is None:
		abort(404)
	return render_template('user.html', user=user, users=users)


#edit user info
@main.route('/eidt-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash('Your profile has been update.')
		return redirect(url_for('.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('The profile of {} has been updated.'.format(user.username))
		return redirect(url_for('.user', username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('edit_profile.html', form=form)















