# Elenchus API

A simple REST-style API built using Python's standard library.

## Requirements

- Python 3.12+

## Installation

Clone the repository and activate a virtual environment.

## Running the server

python3 server.py --port 8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Greeting |
| GET | /courses | List courses |
| GET | /courses/:id | Retrieve a course |
| POST | /courses | Create a course |

## Examples

Include real curl requests and responses for each endpoint.

## Error Responses

Document 400, 404, 405, 411, 415 and other supported errors.

## Architecture

Explain:
- BaseHTTPRequestHandler
- HTTPServer
- In-memory course collection
- JSON serialization
- Content-Length

## Limitations

- Data is stored in memory.
- Restarting the server resets created courses.
- No database or authentication.

## Learning Reflections

Explain what you learned about HTTP, TCP, request parsing,
response headers, status codes and REST-style APIs.