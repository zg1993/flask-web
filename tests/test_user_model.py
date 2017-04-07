#!/usr/bin/env python
#-*- coding: utf-8-*-


import unittest
from app.models import User, Permission



class UserModelTestCase(unittest.TestCase):


	def test_password_setter(self):
		u = User(password='qqq')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='qqq')
		self.assertTrue(u.verify_password('qqq'))
		self.assertFlase(u.verify_password('aaa'))

	def test_password_salts_are_random(self):
		u = User(password='qqq')
		u2 = User(password='aaa')
		self.assertTrue(u.password_hash != u2.password_hash)

	def test_roles_and_permissions(self):
		Role.insert_roles()
		u = User(email='cc@.qq.com', password='cat')
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFlase(u.can(Permission.MODERATE_COMMENTS))

	def test_anonymous_user(self):
		u=AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))