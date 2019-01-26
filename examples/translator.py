#!/usr/local/bin/python3 -tt

"""This is a module for encoding/decoding message between ActorCloud and
devices. This is useful when the messages sent to or from non-reconfigurable devices
are not complied with the data structures defined by the Actor Schema.

The callback functions must be exported in this module are:

- decode(topic, message):
  Called by ActorCloud when a raw message is received from a client, to decode the
  message to the `normative` format according to the schema file.

  Args:
      topic (str): The topic of this message.
      message (bytes): The payload of the message.
  Returns:
      Tuple: (status_code, result)
             `status_code`: integer, 0 - OK, 1 - ERROR.
             `result`: bytes, a JSON string that complies with the data structures
                       defined in the schema file.

- encode(topic, message):
  Called by ActorCloud before a message is going to be sent to a client,
  to encode the message to the format that the client requires.

  Args:
      topic (str): The topic of this message.
      message (str): The payload of the message, this message is of the format
                     defined in the schema file.
  Returns:
      Tuple: (status_code, result)
             `status_code`: integer, 0 - OK, 1 - ERROR.
             `result`: bytes, a message in the format the client requires.
"""

import sys
import json

## define status codes
OK = 0
ERROR = 1

############################################################
## Callbacks
############################################################
"""
To simplify the example, let's assume the message sent from clients
is also of JSON format, but doesn't comply with the schema file:

  Event examples sent from clients:
    [{"tmp": {"ts": 1547660823, "v": -3.7}}
     {"hmd": {"ts": 1547660823, "v": 34}}]

  Response examples sent from clients:
    StatusResult:
      {"req_id": 1, "code": 0, "st": 1}
    TemperatureResult:
      {"req_id": 2, "code": 0, "tmp": {"ts": 1547660823, "v": -3.7}}
    HumidityResult:
      {"req_id": 3, "code": 0, "hmd": {"ts": 1547660823, "v": 34}}

  We need to translate theses messages to right format according to the `schema_design.yaml`.
  See the `events` and `responses` sections in `schema_design.yaml`:

  Then our result message after decoding should be:

  Events:
  { "data_type": "events",
    "data": [
      {"humidity": {"time": 1547660823, "value": 34}},
      {"temperature": {"time": 1547660823, "value": -3.7}}
    ]}

  Responses:
    StatusResult:
      { "data_type": "responses",
        "data": {
          "request_id": 1,
          "result": {"code": 0, "msg": "ok", "is_working": true}
        }
      }
    TemperatureResult:
      { "data_type": "responses",
        "data": {
          "request_id": 2,
          "result": {
            "code": 0,
            "msg": "ok",
            "temperature": {"time": 1547660823, "value": -3.7}
          }
        }
      }
    HumidityResult:
      { "data_type": "responses",
        "data": {
          "request_id": 3,
          "result": {
            "code": 0,
            "msg": "ok",
            "humidity": {"time": 1547660823, "value": 34}
          }
        }
      }
"""
def decode(topic, message):
  """Decode the messages according to the schema

  >>> decode('/19/0/0', '[{"tmp": {"ts": 1547660823, "v": -3.7}}, {"hmd": {"ts": 1547660823, "v": 34}}]')
  (0, '{"data_type": "events", "data": [{"temperature": {"time": 1547660823, "value": -3.7}}, {"humidity": {"time": 1547660823, "value": 34}}]}')

  >>> decode('/19/0/0', '{"req_id": 1, "code": 0, "st": 1}')
  (0, '{"data_type": "responses", "data": {"request_id": 1, "result": {"code": 0, "msg": "ok", "is_working": true}}}')

  >>> decode('/19/0/0', '{"req_id": 2, "code": 0, "tmp": {"ts": 1547660823, "v": -3.7}}')
  (0, '{"data_type": "responses", "data": {"request_id": 2, "result": {"code": 0, "msg": "ok", "temperature": {"time": 1547660823, "value": -3.7}}}}')

  >>> decode('/19/0/0', '{"req_id": 3, "code": 0, "hmd": {"ts": 1547660823, "v": 34}}')
  (0, '{"data_type": "responses", "data": {"request_id": 3, "result": {"code": 0, "msg": "ok", "humidity": {"time": 1547660823, "value": 34}}}}')
  """

  if topic == '/19/0/0':
    try:
      raw_json = json.loads(message)
      if type(raw_json) == list:
        return decode_events(raw_json)
      elif type(raw_json) == dict:
        return decode_responses(raw_json)
    except Exception:
      print("decode error:",)
      return (ERROR, "decode error({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
  else:
    return (ERROR, 'decode error: incorrect_topic')

"""
If the format of requests defined by the schema does not conform to the ones that
devices accept, we need to translate the requests before sending them to the devices.

To simplify the example, we assume the request format used by device is also of
JSON format:

{"cmd": CmdType(string), "req_id": ReqId(integer), "res": ResourceName(string)}

But the request format that defined in the `schema_design.yaml` is:

{ "data_type": "requests",
  "data": {
    "request_type": RequestType(string),
    "request_id": ReqId(integer),
    "parameters": Params(array)
  }
}
"""
def encode(topic, message):
  """Encode the messages that are going to be sent to devices according to the schema

  >>> encode('/19/1/0', '{"data_type": "requests", "data": {"request_type": "get_device_status","request_id": 1,"parameters": []}}')
  (0, '{"cmd": "get", "req_id": 1, "res": "st"}')

  >>> encode('/19/1/0', '{"data_type": "requests", "data": {"request_type": "get_temperature","request_id": 2,"parameters": [{"sensor_id": 0}]}}')
  (0, '{"cmd": "get", "req_id": 2, "res": "tmp", "params": [{"sensor_id": 0}]}')

  >>> encode('/19/1/0', '{"data_type": "requests", "data": {"request_type": "get_humidity","request_id": 3,"parameters": [{"sensor_id": 2}]}}')
  (0, '{"cmd": "get", "req_id": 3, "res": "hmd", "params": [{"sensor_id": 2}]}')
  """

  if topic == '/19/1/0':
    try:
      raw_json = json.loads(message)
      return encode_request(raw_json)
    except Exception:
      print("decode error:",)
      return (ERROR, "decode error({0}): {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
  else:
    return (ERROR, 'decode error: incorrect_topic')

############################################################
## Helper functions
############################################################
def decode_events(events):
  ## translate the raw message
  data = list(map(trans_data, events))
  ## add 'data_type' and wrap the data with 'data' dict
  return (OK, json.dumps({'data_type': 'events', 'data': data}))

def decode_responses(response):
  req_id = response['req_id']
  resp = trans_data(response)
  result = None
  if None == resp:
    result = {'code': response['code'], "msg": "unsupported response: "+str(response)}
  else:
    result = {'code': response['code'],
              'msg': result_msg(response['code']), **resp}
  data = {'request_id': req_id, 'result': result}
  return (OK, json.dumps({'data_type': 'responses', 'data': data}))

def trans_data(data):
  if 'tmp' in data:
    v = data['tmp']
    return {'temperature': {'time': v['ts'], 'value': v['v']}}
  elif 'hmd' in data:
    v = data['hmd']
    return {'humidity': {'time': v['ts'], 'value': v['v']}}
  elif 'st' in data:
    return {'is_working': 1 == data['st']}

def encode_request(request):
  if request['data_type'] == 'requests':
    data = request['data']
    req_base = {'cmd': "get", 'req_id': data['request_id'], 'res': res(data['request_type'])}
    p = params(data)
    return (OK, json.dumps(req_base)) if p == [] else (OK, json.dumps({**req_base, 'params': p}))
  else:
    return (ERROR, 'encode error: not a request - {0}'.format(request['data_type']))

def params(data):
  return data['parameters'] if 'parameters' in data else []

def res(request_type):
  if request_type == 'get_device_status':
    return 'st'
  elif request_type == 'get_temperature':
    return 'tmp'
  elif request_type == 'get_humidity':
    return 'hmd'

def result_msg(code):
  if code == 0:
    return 'ok'
  elif code == 1:
    return 'error'
  elif code == 2:
    return 'pending'

if __name__ == '__main__':
  import doctest
  doctest.testmod()