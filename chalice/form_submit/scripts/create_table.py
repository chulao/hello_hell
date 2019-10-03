import os
import sys
import uuid
import json
import argparse

import boto3

TABLE_NAME_FORMAT = '%s_%s'

TABLES = {
  'users': {
    'prefix': 'form_submit-users',
    'env_var': 'USERS_TABLE_NAME',
    'hash_key': 'email'
  }
}



def get_similar_tables(table_name):
  client = boto3.client('dynamodb')
  tables = client.list_tables()['TableNames']
  return list(filter(lambda t: table_name in t, tables))



def delete_table(table_name):
  client = boto3.client('dynamodb')
  print("---- DELETING TABLE----")
  print("- Name: {}".format(table_name))
  client.delete_table(TableName=table_name)



def create_table(table_name_prefix, stage, hash_key, range_key=None):
  client = boto3.client('dynamodb')

  table_name_format = TABLE_NAME_FORMAT+'-%s'
  table_name = table_name_format % (table_name_prefix, stage, str(uuid.uuid4()))

  print("---- CREATING TABLE----")
  print("- Stage: {}".format(stage))
  print("- Name: {}".format(table_name))

  key_schema = [
    {'AttributeName': hash_key, 'KeyType': 'HASH'}
  ]

  attribute_definitions = [
    {'AttributeName': hash_key, 'AttributeType': 'S'}
  ]

  if range_key is not None:
    key_schema.append({'AttributeName': range_key, 'KeyType': 'RANGE'})
    attribute_definitions.append({'AttributeName': range_key, 'AttributeType': 'S'})

  client.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput={
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5,
    }
  )

  waiter = client.get_waiter('table_exists')
  waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
  return table_name



def record_as_env_var(key, value, stage):
  config_file = os.path.join('..', '.chalice', 'config.json')

  with open(config_file) as f:
    data = json.load(f)
    data['stages'].setdefault(stage, {}).setdefault('environment_variables', {})[key] = value

  with open(config_file, 'w') as f:
    serialized = json.dumps(data, indent=2, separators=(',', ': '))
    f.write(serialized + '\n')



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--stage', default='dev')
  parser.add_argument('-t', '--table-type', default='users', choices=['users'], help='Specify which type to create')

  args = parser.parse_args()
  table_config = TABLES[args.table_type]

  table_name = TABLE_NAME_FORMAT % (table_config['prefix'], args.stage)

  similar_tables = get_similar_tables(table_name)
  recreate = 'R'
  if len(similar_tables) == 1:
    print('# There are one table similiar with {}'.format(len(similar_tables), table_name))
    print('> {}'.format(similar_tables[0]))
    recreate = input('# Should abort (A) or recreate it (R) [default A]: ')
  elif len(similar_tables) > 1:
    print('# Were found {} tables similiar with {}'.format(len(similar_tables), table_name))
    print('Aborting execution.....')
    sys.exit()


  if recreate == 'r' or recreate == 'R':
    if len(similar_tables) == 1:
      delete_table(similar_tables[0])

    table_name = create_table(table_config['prefix'], args.stage, table_config['hash_key'], table_config.get('range_key'))
    record_as_env_var(table_config['env_var'], table_name, args.stage)


if __name__ == '__main__':
  main()