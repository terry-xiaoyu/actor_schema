# actor_schema

Schema design for Actor Cloud.

Actor schema is a specification doc for defining the data structures used in IoT device management procedures.

The main 3 data types are:

- events: the event reports come from the devices
- requests: the requests (or commands) sent from IoT platform to the devices
- responses: the responses replied by the clients

The basic syntax is inspired by the [OpenAPI](https://github.com/OAI/OpenAPI-Specification).

## Data Types

Supported data types are the same as the [Data Types supported by OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#dataTypes):
[`type`](#dataTypes) | [`format`](#dataTypeFormat) | Comments
------ | -------- | --------
`integer` | `int32` | signed 32 bits
`integer` | `int64` | signed 64 bits (a.k.a long)
`number` | `float` | |
`number` | `double` | |
`string` | | |
`string` | `byte` | base64 encoded characters
`string` | `binary` | any sequence of octets
`boolean` | | |
`string` | `date` | As defined by `full-date` - [RFC3339](https://xml2rfc.ietf.org/public/rfc/html/rfc3339.html#anchor14)
`string` | `date-time` | As defined by `date-time` - [RFC3339](https://xml2rfc.ietf.org/public/rfc/html/rfc3339.html#anchor14)
`string` | `password` | A hint to UIs to obscure input.