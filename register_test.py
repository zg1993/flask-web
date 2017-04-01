#!/usr/bin/env python
#-*- coding: utf-8-*-


from app.models import User
from app import db

users = []
for m, n in enumerate(range(20)):
	user = User(username='ssb'+str(m), password=str(n), email='sss'+str(n)+'@'+str(n)+'.com')
	users.append(user)
db.session.add_all(users)
db.session.commit()




