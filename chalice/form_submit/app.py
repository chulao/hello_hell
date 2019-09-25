from os import environ
from urllib.parse import parse_qs
import json
import csv

from chalice import Chalice, Response
from chalice import BadRequestError

from data import Data, InMemoryDB, DynamoDB
from templates import render


app = Chalice(app_name='form_submit')
_DB = None

def get_app_db():
  global _DB
  if _DB is None:
    table_name = environ['TABLE_NAME']
    if table_name == 'InMemory':
      _DB = InMemoryDB({
        'user': {
          'test1@test.com': {'email': 'test1@test.com', 'fullname': 'Test1', 'phone': '(11) 12345-1111'},
          'test2@test.com': {'email': 'test2@test.com', 'fullname': 'Test2', 'phone': '(11) 12345-2222'},
          'test3@test.com': {'email': 'test3@test.com', 'fullname': 'Test3', 'phone': '(11) 12345-3333'},
        }
      })
    else:
      _DB = DynamoDB(table_name)
  return _DB


def read_user(data):
  user = {}
  data.read(user, 'email')
  data.read(user, 'fullname')
  data.read(user, 'phone')
  return user


@app.route('/')
def index():
  template = render('./templates/user.html', {})
  return Response(template, status_code=200, headers={'Content-Type': 'text/html', 'Access-Control-Allow-Origin': '*'})


@app.route('/users', methods=['GET'], cors=True)
def list_users():
  response_type = app.current_request.query_params['type'] if app.current_request.query_params and 'type' in app.current_request.query_params else 'json'
  app.log.debug('List users in {} format'.format(response_type))
  users = get_app_db().list()
  if response_type == 'json':
    data = json.dumps(list(users))
  else:
    data = ';'.join(list(users)[0].keys()) + '\n'
    for user in list(users):
      data = data + ';'.join(user.values()) + '\n'
  return data


@app.route('/users', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def create_user():
  app.log.debug("Creating user")
  user = {}

  if ('content-type' in app.current_request.headers) :
    content_type = app.current_request.headers['content-type']
    if content_type == 'application/json':
      user = read_user(Data(app))
    else: 
      user = read_user(Data(app, True))
  else:
      user = read_user(Data(app))

  record = get_app_db().get(user['email'])

  if record:
    template = render('./templates/error.html', {})
    return Response(template, status_code=409, headers={'Content-Type': 'text/html', 'Access-Control-Allow-Origin': '*'})
  else:
    template = render('./templates/success.html', {})
    return Response(template, status_code=200, headers={'Content-Type': 'text/html', 'Access-Control-Allow-Origin': '*'})



