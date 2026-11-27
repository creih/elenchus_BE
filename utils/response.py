import json


def send_json(handler, status_code, json_data, extra_headers=None):
    body = json.dumps(json_data).encode("utf-8")

    handler.send_response(status_code)

    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8"
    )

    handler.send_header(
        "Content-Length",
        str(len(body))
    )

    if extra_headers:
        for header, value in extra_headers.items():
            handler.send_header(header, value)

    handler.end_headers()
    handler.wfile.write(body)
