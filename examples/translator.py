#!/usr/bin/python -tt

"""This is a module for encoding/decoding message between ActorCloud and
devices. This is useful when the messages sent to or from devices are not
complied with the data structures defined by the Actor Schema.

The callback functions must be exported in this module are:

- decode(topic, raw_message):
  Called when a raw message is received from a client, to decode the
  message to the `normative` format according to the schema file.

  Args:
      topic (str): The topic of this message.
      raw_message (bytes): The payload of the message.
  Returns:
      str: The return value. A JSON string complies to the data structures
           defined in the schema file.

- encode(topic, message):
  Called before a message is going to be sent to a client, to encode the message
  to the format that the client requires.

  Args:
      topic (str): The topic of this message.
      message (str): The payload of the message, this message is of the format
                     defined in the schema file.
  Returns:
      bytes: The return value. The message in the format the client requires.

"""

import sys
import json

OK = 0
ERROR = 1

def decode(topic, raw_message):
  '''To simplify the example, the raw_message sent from clients is of JSON format:

  Events sent from clients:
    [{"tmp": {"ts": 1547660823, "v": -3.7}}
     {"hmd": {"ts": 1547660823, "v": 34}}]

  We need to translate this message to the right format according to the `schema_design.yaml`, see the `events` section in `schema_design.yaml`.

  Our result message should be:
  { "data_type": "events",
    "data": [
      {"humidity": {"time": 1547661822, "value": 100}},
      {"temperature": {"time": 1547660823, "value": -3.7}}
    ]}
  '''

  if topic == '/19/0/0':
    raw_json = json.loads(raw_message)
    if type(raw_json) == list:
      return decode_events(raw_json)
    elif type(raw_json) == dict:
      return decode_responses(raw_json)
  else:
    return (ERROR, 'incorrect topic')

def encode(topic, message):
  return (ERROR, 'not implemented')

## Helper functions

def decode_events(raw_json):
  data = []
  ## translate the raw message
  for event in raw_json:
    if 'tmp' in event:
      v = event['tmp']
      data.append({'temperature': {'time': v['ts'], 'value': v['v']}})
    elif 'hmd' in event:
      v = event['hmd']
      data.append({'humidity': {'time': v['ts'], 'value': v['v']}})
  ## add 'data_type' and wrap the data with 'data' dict
  return (OK, json.dumps({'data_type': 'events', 'data': data}))

def decode_responses(raw_json):
  return (ERROR, 'not implemented')