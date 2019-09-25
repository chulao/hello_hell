from urllib.parse import parse_qs
import boto3


__all__ = ['Data', 'InMemoryDB', 'DynamoDB']



class Data(object):
  def __init__(self, app, form=False):
    self._json_type = not form
    self._data = app.current_request.json_body if not form else parse_qs(app.current_request.raw_body.decode())

  def get(self, name):
    value = self._data.get(name)
    return value if self._json_type else value[0]

  def read(self, item, name):
    item[name] = self.get(name)



class UserData(object):
  def get(self, email):
    pass

  def save(self, data):
    pass



class InMemoryDB(UserData):
  def __init__(self, state=None):
    if state is None:
      state = {}
    print('InMemoryDB.state: {}'.format(state))    
    self._state = state

  def get(self, email):
    print('InMemoryDB.get: {}'.format(email))    
    if 'user' not in self._state:
      self._state['user'] = {}
    return self._state['user'][email] if email in self._state['user'] else None

  def save(self, data):
    print('InMemoryDB.save: {}'.format(data['email']))
    if 'email' not in data:
      raise KeyError('Not found email into data')
    if 'user' not in self._state:
      self._state['user'] = {}
    self._state['user'][data['email']] = data



class DynamoDB(UserData):
  def __init__(self, table_name):
    dynamodb = boto3.resource("dynamodb")
    self._table = dynamodb.Table(table_name)

  def get(self, email):
    response = self._table.get_item(
      Key={
        'email': email,
      },
    )
    return response['Item']

  def save(self, data):
    self._table.put_item(Item=data)