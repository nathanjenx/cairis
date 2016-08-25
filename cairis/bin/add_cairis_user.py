#!/usr/bin/python
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import argparse
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.cors import CORS
from cairis.core.Borg import Borg
import cairis.core.BorgFactory

__author__ = 'Shamal Faily'

cairis.core.BorgFactory.dInitialise()
app = Flask(__name__)
app.config['DEBUG'] = True
b = Borg()
import pytest 
pytest.set_trace()
app.config['SECRET_KEY'] = b.secretKey
app.config['SECURITY_PASSWORD_HASH'] = b.passwordHash
app.config['SECURITY_PASSWORD_SALT'] = b.passwordSalt
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + b.auth_dbUser + ':' + b.auth_dbPasswd + '@' + b.auth_dbHost + '/' + b.auth_dbName

db = SQLAlchemy(app)
cors = CORS(app)

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('auth_user.id')), db.Column('role_id', db.Integer(), db.ForeignKey('auth_role.id')))

class Role(db.Model, RoleMixin):
  __tablename__ = 'auth_role'
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  __tablename__ = 'auth_user'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app, user_datastore)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Add CAIRIS user')
  parser.add_argument('user',help='Email address')
  parser.add_argument('password',help='password')
  args = parser.parse_args()

  db.create_all()
  user_datastore.create_user(email=args.user, password=args.password) 
  db.session.commit()

