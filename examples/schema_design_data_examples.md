# Data examples

This file contains some data examples that complies with the schema_design.yaml

## event examples

- temperature events:

```json
{
  "data_type": "events",
  "data": [
    {"temperature": {"time": 1547660823, "value": -3.7}}
  ]
}
```

- humidity events:

```json
{ "data_type": "events",
  "data": [
    {"humidity": {"time": 1547661822, "value": 100}}
  ]
}
```

- containing both humidity and temperature in a single event report:

```json
{
  "data_type": "events",
  "data": [
    {"humidity": {"time": 1547661822, "value": 100}},
    {"temperature": {"time": 1547661822, "value": -3.7}}
  ]
}
```

## request examples

- `get_device_status` request

```json
{
  "data_type": "requests",
  "data": {
    "request_type": "get_device_status",
    "request_id": 1,
    "parameters": []
  }
}
```

- `get_temperature` request

```json
{
  "data_type": "requests",
  "data": {
    "request_type": "get_temperature",
    "request_id": 2,
    "parameters": [{"sensor_id": 0}]
  }
}
```

- `get_humidity` request

```json
{
  "data_type": "requests",
  "data": {
    "request_type": "get_humidity",
    "request_id": 3,
    "parameters": [{"sensor_id": 0}]
  }
}
```

## responses examples

- response of `get_device_status`

```json
{
  "data_type": "responses",
  "data": {
    "request_id": 1,
    "result": {
      "result_code": "ok",
      "is_working": true
    }
  }
}
```

- response of `get_temperature`

```json
{
  "data_type": "responses",
  "data": {
    "request_id": 2,
    "result": {
      "result_code": "ok",
      "temperature": {
        "time": 1547660823,
        "value": -3.7
      }
    }
  }
}
```

- response of `get_humidity`

```json
{
  "data_type": "responses",
  "data": {
    "request_id": 3,
    "result": {
      "result_code": "ok",
      "humidity": {
        "time": 1547661822,
        "value": 100
      }
    }
  }
}
```