import jsonschema
from jsonschema import validate

CLIENTS_POST = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 50},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "number"},
        "requirement": {"type": "string"},
    },
    "required": ["name", "email", "requirement"]
}

CLIENTS_PATCH = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 50},
        "age": {"type": "number"},
        "requirement": {"type": "string"},
    },
    "additionalProperties": False
}


def schema_validation(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        print("Validation successful. The JSON data is valid.")
        return None
    except jsonschema.exceptions.ValidationError as ve:
        print("Validation error:")
        print(ve)
        return ve