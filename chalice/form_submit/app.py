from os import environ
from urllib.parse import parse_qs

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
      _DB = InMemoryDB({'user': {'test@test.com': {'email': 'test@test.com', 'fullname': 'Test', 'phone': '(11) 12345-1234'}}})
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


@app.route('/user', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
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



