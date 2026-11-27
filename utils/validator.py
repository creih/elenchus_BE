import json


def parse_json(body):
    try:
        return json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid JSON")


def validate_json_object(data):
    if not isinstance(data, dict):
        raise ValueError(
            "Request body must be a JSON object"
        )

    return data