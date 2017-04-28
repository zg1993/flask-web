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
from flask import request
from flask import jsonify
from flask import make_response


@main.route('/', methods=['GET', 'POST'])
def index():
	print('index')
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data, au=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	#posts = Post.query.order_by(Post.timestamp.desc()).all()
	page = request.args.get('page', 1, type=int)
	# pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
	# 	page, per_page=10, error_out=True)
	#add show followed post
	show_followed = False
	if current_user.is_authenticated:
		show_followed = bool(request.cookies.get('show_followed', ''))
	if show_followed:
		query = current_user.followed_posts
	else:
		query = Post.query
	pagination = query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=10,
		error_out=True)
	posts = pagination.items
	return render_template('index.html', 
							form=form, 
							show_followed=show_followed, 
							posts=posts,
							pagination=pagination)
	#return render_template('index.html', form=form, posts=posts)


@main.route('/all')
@login_required
def show_all():
	resp = make_response(redirect(url('.index')))
	resp.set_cookie('show_followed', '', max_age=30*24*60*60)
	return resp


@main.route('/followed')
@login_required
def show_followed():
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
	return resp


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
	#posts = user.posts.order_by(Post.timestamp.desc()).all()
	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, per_page=5, error_out=False)
	posts = pagination.items
	return render_template('user.html', user=user, users=users, posts=posts, pagination=pagination)


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


#post 
@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', posts=[post])


#post edit
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Post.query.get_or_404(id)
	if current_user != post.au and \
		not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash('The post has been updated.')
		return redirect(url_for('.post', id=post.id))
	form.body.data = post.body
	return render_template('post_edit.html', form=form)


#follow
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('invalid user.')
		return redirect(url_for('.index'))
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('.user', username=username))
	current_user.follow(user)
	flash('You are now following this {}.'.format(username))
	print('follow successed!')
	return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('invalid user.')
		return redirect(url_for('.index'))
	if not current_user.is_following(user):
		flash('You are not following this user.')
		return redirect(url_for('.user', username=username))
	current_user.unfollow(user)
	flash('You are now unfollowing this {}.'.format(username))
	return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('invalid user.')
		return redirect(url_for('.index'))
	# page = request.args.get('page', 1, type=int)
	# pagination = user.followers.paginate(
	# 	page, per_page=10,
	# 	error_out=False)
	# follows = [{'user': item.follower, 'timestamp': item.timestamp}
	# 			for item in pagination.items]
	following = user.followers.all()
	return render_template('followers.html', user=user, title='的关注者',
							follows=following)


@main.route('/followed_by/<username>')
def followed_by(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('invalid user.')
		return redirect(url_for('.index'))
	# page = request.args.get('page', 1, type=int)
	# pagination = user.followers.paginate(
	# 	page, per_page=10,
	# 	error_out=False)
	# followed = [{'user': item.followed, 'timestamp': item.timestamp}
	# 			for item in pagination.items]
	followed = user.followed.all()
	return render_template('followed_by.html', user=user, title='关注的人',
							follows=followed)


@main.route('/_add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a+b)

@main.route('/a')
def index1():
	return render_template('test.html')