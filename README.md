# actor_schema

Schema design for Actor Cloud.

Actor schema is a specification doc for defining the data structures used in IoT device management procedures.

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

## Translators

If the messages that the devices use are not comply to the data structures defined in the schema file, we could write `translators` to decode/encode between ActorCloud and devices.

Translator is a python module contains callbacks for decoding the events/responses from the device as well as encoding the requests to the device.

An example translator is provided in `examples/translator.py`.
