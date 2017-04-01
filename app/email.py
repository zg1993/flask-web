#!/usr/bin/env python
#-*- coding: utf-8-*-


from flask import render_template
from flask_mail import Message
from config import config
from . import mail
from threading import Thread
from manage import app 


def send_async_email(msg):
	with app.app_context():
		mail.send(msg)


def send_email(to, subject, template, **kwargs):
	msg = Message(config['default'].FLASKY_MAIL_SUBJECT_PREFIX+subject,
					sender=config['default'].FLASKY_MAIL_SENDER,
					recipients=[to])
	msg.body = render_template(template+'.txt', **kwargs)
	msg.html = render_template(template+'.html', **kwargs)
	thr = Thread(target=send_async_email, args=(msg,))
	thr.start()
	return thr

