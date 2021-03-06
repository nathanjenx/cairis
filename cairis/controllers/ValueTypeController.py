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

import sys
if (sys.version_info > (3,)):
  import http.client
  from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
else:
  import httplib
  from httplib import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from flask import session, request, make_response
from flask_restful import Resource
from cairis.data.ValueTypeDAO import ValueTypeDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ValueTypeMessage
from cairis.tools.ModelDefinitions import ValueTypeModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ValueTypesAPI(Resource):

  def get(self,type_name,environment_name):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    if environment_name == 'all':
      environment_name = ''
    vts = dao.get_value_types(type_name,environment_name)
    dao.close()

    resp = make_response(json_serialize(vts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


class ValueTypesCreateAPI(Resource):

  def post(self):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    new_vt = dao.from_json(request)
    dao.add_value_type(new_vt)
    dao.close()

    resp_dict = {'message': 'Value Type successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ValueTypesByNameAPI(Resource):

  def get(self, type_name,environment_name,object_name):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    found_vt = dao.get_value_type(type_name,environment_name,object_name)
    dao.close()

    resp = make_response(json_serialize(found_vt, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


  def put(self, type_name, environment_name, object_name):
    session_id = get_session_id(session, request)
    dao = ValueTypeDAO(session_id)
    upd_vt = dao.from_json(request)
    dao.update_value_type(upd_vt, type_name, environment_name, object_name)
    dao.close()

    resp_dict = {'message': 'Value Type successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, type_name, environment_name, object_name):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    dao.delete_value_type(type_name,environment_name,object_name)
    dao.close()

    resp_dict = {'message': 'Value Type successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
