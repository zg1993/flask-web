#!/usr/bin/env python
#-*- coding: utf-8-*-

#from FlaskForm import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User
from wtforms import ValidationError


class NameForm(FlaskForm):
	name = StringField('name:', validators = [Required()])
	submit = SubmitField('submit')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me log in')
	submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('username', validators=[
		Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z_.]*$', 0, 'invalid format')])
	password = PasswordField('password', validators=[
		Required(), EqualTo('password2', message='Password must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')


	# def validate_email(self, field):
	# 	if User.query.filter_by(email=field.data).first():
	# 		raise ValidationError('Email already registered.')

	# def validate_username(self, field):
	# 	if User.query.filter_by(username=field.data).first():
	# 		raise ValidationError('Username already in use.')

