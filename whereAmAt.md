This is a solid first backend project. The central idea behind Project 0x00: The Raw Server (elenchus) is to understand HTTP by building an API without relying on a framework.

You have until Wednesday, 25 November 2026, at 14:00 Kigali time for full marks. Since today is Monday, 23 November, you have roughly two days to complete it.

I'd approach this as a learning project, not just a race to finish eight tasks.

1. What you need to build
You're building a small REST-style API for managing courses.

Elenchus API

Python 3.12+
SERVER

http.server + BaseHTTPRequestHandler

No Flask, FastAPI, Django or database.

API endpoints

GET /

Hello
GET /courses

List
GET /courses/:id

Single
POST /courses

Create
In-memory course collection

Python list or dictionary. No database.

2. Recommended project structure
Since the assignment recommends separate backend and frontend repositories, I'd choose the polyrepo approach.


text
elenchus-api/
│
├── notes/
│   ├── http-history.md
│   ├── http-messages.md
│   ├── http-1x.md
│   ├── software-design-1.md
│   └── software-design-2.md
│
├── server.py
├── courses.py
├── README.md
├── requirements.txt
└── .gitignore
You can start with a single server.py and introduce additional files when separation becomes useful.

3. Your task-by-task roadmap
Here is the order I'd follow.

Mandatory task tracker

0/8 completed
0/100

Task 0: Setup

Create GitHub repository, virtual environment, README and .gitignore.

10 pts


Task 1: Hello

Start an HTTP server on a configurable port and implement GET /.

10 pts


Task 2: List courses

Return at least five in-memory courses as JSON.

15 pts


Task 3: Single course

Parse /courses/:id manually and distinguish 400 from 404.

15 pts


Task 4: Create course

Read Content-Length, parse JSON, validate input and return 201 with Location.

25 pts


Task 5: Method discipline

Implement 405, Allow and proper unknown-path handling.

10 pts


Task 6: Logging

Log method, path, status and request duration.

5 pts


Task 7: README

Document endpoints, real curl transcripts and your learning reflections.

10 pts

4. Important concepts you must understand
These are particularly important because your checker will quiz you.

Concept

What you should understand

HTTP request

Method, path, headers and optional body

HTTP response

Status line, headers and optional body

Statelessness

Each HTTP request is independent; the server doesn't inherently remember previous requests

JSON

A standard format for exchanging structured data

Content-Length

Declares the number of bytes in the request body

HTTP 400

The request is malformed or invalid

HTTP 404

The requested resource doesn't exist

HTTP 201

A resource was successfully created

HTTP 405

The method isn't supported for that resource

HTTP 415

The request uses an unsupported media type

HTTP 500

An unexpected server-side error occurred

Location

Identifies the newly created resource

Integer money

Avoids floating-point precision errors

A particularly important design decision: money
Don't store course prices like this:


python
price = 19.99
Floating-point arithmetic can introduce precision errors.

Instead, store money in the smallest currency unit:


python
price_cents = 1999
Or, for Rwandan francs:


python
price_rwf = 15000
Your API can explain that prices are represented as integer currency units.

Another important concept: Content-Length
When a client sends:


http
POST /courses HTTP/1.1
Content-Type: application/json
Content-Length: 39
The server must read exactly the declared number of bytes.

This is important because the request body might arrive in multiple network packets. One read() operation for an arbitrary amount of data is not a reliable way to determine where the body ends.

5. Suggested schedule
Monday, 23 November

Read HPBN chapters 9 and 11.

Set up GitHub and your virtual environment.

Complete Tasks 0 and 1.

Tuesday, 24 November

Complete Tasks 2 and 3.

Spend focused time on Task 4.

Test using real curl.

Wednesday, 25 November

Finish Task 4 if necessary.

Complete Tasks 5 and 6.

Write README and Rubber Duck answers.

Push and submit before 14:00.

Don't sacrifice mandatory tasks for advanced bonuses. Your first target is 100%.

6. How I'd like you to approach this project
Your assignment explicitly says that when you're stuck, you'll receive questions and hints rather than complete fixes.

I'd follow that approach.

For every task:

Read the relevant documentation.

Explain the concept in your own words.

Implement it yourself.

Test it with curl.

Commit your work with a meaningful Git message.

Explain why your implementation works.

For example:


bash
git add .
git commit -m "feat: implement course listing endpoint"
7. Let's start with Task 0
Before writing the server, I want to establish your current understanding.

First question:

What do you understand by an HTTP server?

Explain it in your own words, even if you're not completely sure. I'll help identify gaps, then we'll work through setting up your elenchus-api repository.

The goal is that by the end of this project, you can explain what happens between typing a URL in a browser and receiving a response, without needing to look at your notes.


is a computer that can respond to requests for hypertext as its built on tcp and is meant to provide responses with certain format like html formated responses amongst others,providing relevant headers and methods to manipulate said data

Good! You're already thinking in the right direction. You understand that an HTTP server receives requests, communicates over TCP, and sends structured responses.

Let's sharpen your explanation a little.

1. What you got right
Responding to requests: Correct. An HTTP server listens for incoming HTTP requests and sends responses.

TCP: Correct for HTTP/1.1 and HTTP/2, which commonly use TCP as their transport protocol. HTTP/3 uses QUIC over UDP.

Response formats: Correct. Responses can contain HTML, JSON, plain text, images, and other data formats.

Headers: Correct. Headers carry metadata about the request or response.

Methods: Correct. Methods such as GET, POST, PUT and DELETE communicate the intended operation.

2. One important distinction
An HTTP server doesn't necessarily serve hypertext.

HTTP stands for Hypertext Transfer Protocol, but today it is used to transfer much more than hypertext.

For example:

HTML for web pages.

JSON for APIs.

Images and videos.

Plain text.

Files and documents.

Also, HTTP methods don't directly manipulate data themselves. They communicate the client's intended action to the server, which decides how to handle it.

3. Your refined rubber-duck explanation
You could explain it like this:

An HTTP server is a software application that listens for incoming HTTP requests from clients. It processes those requests based on their methods, paths, headers and optional bodies, then sends back structured HTTP responses containing a status code, headers and potentially a response body. HTTP/1.1 and HTTP/2 commonly use TCP for communication, while HTTP/3 uses QUIC over UDP. HTTP supports exchanging different kinds of data, including HTML, JSON, images and plain text.

4. Let's test your understanding
Imagine you type https://example.com into your browser.

Walk me through what you think happens between:

You pressing Enter.

The browser communicating with the server.

The server processing the request.

The browser displaying the response.

One question to think about: Does the browser send the entire webpage request as one big piece of information, or does it send a structured HTTP message containing different parts?

Don't worry about getting everything right. We're building your understanding step by step.


1. pressing enter, first of all makes the tcp initiate the three handshake with example.com, then browser sends the method, path and request body or payload optionally and then the server reviews the incoming request and provides appropriate response body, header, once the response reaches the browser from example.com your browser handles the way you see it, the style and if your javascript is enabled adds some additional level of interaction with the displayed data

Excellent. You're connecting the different layers now: transport, HTTP, server processing and browser rendering. That's exactly what I want you to understand before implementing Elenchus.

Your explanation is mostly correct. Let's refine a few details.

1. What you got right
TCP handshake: Correct for HTTP/1.1 and HTTP/2 over TCP.

HTTP request: Correct. The browser sends a method, path, headers and optionally a body.

Server processing: Correct. The server interprets the request and determines the appropriate response.

HTTP response: Correct. The response contains a status code, headers and potentially a body.

Browser rendering: Correct. The browser interprets the received content and renders it. JavaScript can add dynamic behaviour and interaction.

2. Three things to improve
A. DNS happens before the TCP connection.

When you enter https://example.com, the browser needs to discover the server's IP address.

A simplified sequence is:

Browser checks its caches.

DNS resolution obtains an IP address if needed.

Browser establishes a connection.

TLS negotiation establishes a secure connection for HTTPS (for TCP-based HTTPS).

Browser sends the HTTP request.

Remember that HTTP/3 uses QUIC, so its connection establishment differs.

B. The browser doesn't necessarily send a request body.

For example:


http
GET /courses HTTP/1.1
Host: localhost:8000
Accept: application/json
This request has no body.

But a POST request might look like:


http
POST /courses HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 34

{"title":"Python","price":15000}
Notice the distinction between headers and the body.

C. The server doesn't send the webpage's appearance.

The server sends resources, such as HTML, CSS, JavaScript and images.

The browser interprets these resources and constructs the visual page.

3. Let's check whether you've understood HTTP messages
Imagine this request reaches your Elenchus server:


http
POST /courses HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 35

{"title":"Python","price":15000}
I want you to identify four things:

What is POST?

What is /courses?

What is Content-Type telling the server?

Why does the server need Content-Length before reading the body?

Bonus question: What do you think would happen if the server tried to read the request body without knowing how many bytes belong to it?

Take your time. These questions lead directly into Task 4, the most heavily weighted task in your project.


1. post :is the method telling the server normally to write or create new course
2. /courses: is the path of where the post needs to be made
3. content-type: describes the format of the body
4. to know when the body ends and know if every pacjet arrived or some got lost so i t can request a resend
5. if it did that it wouldn't know if the body arrived in full or some packets where lost

Very good! You're beginning to understand the reasoning behind HTTP rather than just memorizing its terminology.

I'd give you 4/5 on this exercise, with one important misconception to correct before we move forward.

1. Reviewing your answers
Question

Assessment

Feedback

POST

Correct

Requests creation or processing of submitted data.

/courses

Correct

Identifies the target resource.

Content-Type

Correct

Describes the media type of the request body.

Content-Length

Mostly
correct

Specifies the number of bytes in the body.

Missing body length

Needs
correction

Knowing the body length isn't the same as detecting lost network packets.

2. Important correction: Content-Length and packet loss
You said:

To know if every packet arrived or some got lost so it can request a resend.

This is the part I want you to reconsider.

TCP already handles reliable delivery when HTTP/1.1 or HTTP/2 uses TCP.

TCP takes care of:

Sequencing data.

Detecting missing data.

Retransmitting lost segments.

Delivering an ordered byte stream to the application.

Content-Length serves a different purpose.

It tells the HTTP server exactly how many bytes belong to the request body.

For example:


http
POST /courses HTTP/1.1
Content-Type: application/json
Content-Length: 35

{"title":"Python","price":15000}
The server knows it must read exactly 35 bytes.

Consider this Python code:


python
content_length = int(self.headers.get("Content-Length", 0))

body = self.rfile.read(content_length)
The server reads the declared number of bytes rather than guessing where the body ends.

If fewer bytes arrive than declared, the read can block waiting for more data or encounter an incomplete connection. TCP handles transport reliability; your application must still handle incomplete or invalid requests appropriately.

3. One more concept: HTTP is stateless
This is one of your project's learning objectives.

Imagine:

You request GET /courses.

The server returns five courses.

You request GET /courses/2.

Does the server inherently remember that you previously requested the course list?

No.

HTTP is stateless: each request is independent. The server doesn't automatically retain the context of previous requests.

Applications can introduce state using mechanisms such as:

Cookies.

Session identifiers.

Authentication tokens.

Databases.

But those are additional mechanisms, not automatic HTTP behaviour.

4. Your next challenge
Before we start Task 0, answer this scenario:

Imagine two clients send requests to your Elenchus API.

Client A sends POST /courses to create Python.

Client B sends POST /courses to create JavaScript.

Both requests arrive almost simultaneously.

Question: If your server stores courses in a Python list, what could potentially go wrong if both requests attempt to modify that list at the same time?

Think about shared memory and concurrency.

I want you to reason through this because your checker explicitly mentions simultaneous course creation.


well there would be an issue with indexes i believe

Good instinct! You're thinking about the shared data structure, which is the right place to investigate. However, indexes aren't necessarily the main problem.

Let's examine it.

1. Imagine our courses list

python
courses = [
    {"id": 1, "title": "Python"},
    {"id": 2, "title": "HTML"}
]
Two clients arrive almost simultaneously:

Client A wants to create JavaScript.

Client B wants to create CSS.

Suppose your server generates IDs using:


python
new_id = len(courses) + 1
What happens if both requests read len(courses) before either adds its course?

Both could calculate:


python
new_id = 3
Now you have two courses with the same ID.

Potential race condition
This is called a race condition: the outcome depends on the timing and ordering of concurrent operations.

2. Is the list itself necessarily unsafe?
Not necessarily.

Python's built-in list supports individual operations such as append(), but that doesn't automatically make a sequence of operations atomic.

For example:


python
new_id = len(courses) + 1
courses.append({
    "id": new_id,
    "title": title
})
The combination of calculating an ID and appending a course is not guaranteed to be atomic.

A lock (threading.Lock) can protect that critical section.

3. Your next question
Let's test whether you've understood the distinction.

Suppose we replace the ID generation with:


python
import itertools

id_counter = itertools.count(1)
And generate IDs using:


python
new_id = next(id_counter)
Question: Does this completely solve the simultaneous creation problem, or do we still need to think about protecting our shared courses list?

Explain your reasoning. Don't worry about getting it perfect.


idk what itertools is or how it works, but you can start guiding me through task 1

Absolutely. We don't need to understand itertools yet. We'll encounter concurrency properly when we reach course creation.

Let's move to Task 1: Hello.

The objective is simple: build a Python HTTP server that listens on a configurable port and responds to GET / with a plain-text greeting and correct HTTP headers.

Task 1 · 10 points
1. Understand what we're building
When someone visits:


text
http://localhost:8000/
Your server should respond with something like:


http
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12
Content-Type: text/plain
Content-Length: 18

Hello from Elenchus
The exact server header and HTTP version may vary.

Notice three important things:

200 OK: The request succeeded.

Content-Type: text/plain: The response body is plain text.

Content-Length: The number of bytes in the response body.

2. First, prepare your project
Open your terminal.

Create your project directory:


bash
mkdir elenchus-api
cd elenchus-api
Create a virtual environment:


bash
python3 -m venv .venv
Activate it.

Linux/macOS:


bash
source .venv/bin/activate
Windows PowerShell:


powershell
.venv\Scripts\Activate.ps1
Create your initial files:


bash
touch server.py README.md .gitignore
On Windows, you can create these files using your editor instead.

Your structure should look like:


text
elenchus-api/
├── .venv/
├── server.py
├── README.md
└── .gitignore
Add this to .gitignore:


gitignore
.venv/
__pycache__/
*.py[cod]
.env
3. Understand the Python tools we'll use
Python's standard library gives us everything needed.

There are three important components:

Component

Responsibility

HTTPServer

Creates and runs the HTTP server.

BaseHTTPRequestHandler

Handles incoming HTTP requests.

self.send_response()

Sends an HTTP status code.

self.send_header()

Adds response headers.

self.end_headers()

Marks the end of the response headers.

self.wfile.write()

Writes the response body.

The architecture looks like this:

HTTP client

curl / Browser

HTTPServer

Listens on port 8000

BaseHTTPRequestHandler

Receives and dispatches requests

do_GET()

Your implementation of GET /

4. Your first implementation challenge
I don't want to dump the complete solution on you. Let's build it incrementally.

Open server.py.

Your first challenge is to write the imports:

Import HTTPServer.

Import BaseHTTPRequestHandler.

Then create a class called RequestHandler that inherits from BaseHTTPRequestHandler.

The structure should look like this:


python
from http.server import ...

class RequestHandler(...):
    pass
Your first checkpoint
Complete the missing imports and inheritance yourself.

Then answer this:

Why do you think we inherit from BaseHTTPRequestHandler instead of writing an entirely new class that handles raw incoming network connections?

Hint: Think about the work Python's standard library has already done for us.

Once you get this checkpoint right, we'll implement do_GET(), configure the port, start the server and test it using real curl.

Don't rush. The purpose of this project is to understand what frameworks normally hide from you.


no can we see the full implementation then ask me on that

Absolutely. Let's look at the complete implementation first, understand every part, and then I'll quiz you on it.

We'll keep it simple for Task 1. No unnecessary abstractions.

Task 1: Complete HTTP server implementation
Create server.py:


python

from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            message = "Hello from Elenchus"
            body = message.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:
            message = "Not Found"
            body = message.encode("utf-8")

            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(
        description="Elenchus HTTP Server"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on"
    )

    args = parser.parse_args()

    server_address = ("", args.port)

    httpd = HTTPServer(server_address, RequestHandler)

    print(f"Elenchus server running on port {args.port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
1. Understand the implementation
Let's break it down.

A. Imports

python
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
HTTPServer: Creates the HTTP server and listens for connections.

BaseHTTPRequestHandler: Provides the machinery for interpreting HTTP requests and dispatching methods.

argparse: Allows us to configure the server through command-line arguments.

Python has already implemented much of the HTTP protocol handling for us.

That's one of the things you're learning: understanding what a framework or library saves you from doing.

B. The RequestHandler class

python
class RequestHandler(BaseHTTPRequestHandler):
We're inheriting from Python's existing request handler.

This gives us methods and attributes such as:

Attribute/method

Purpose

self.path

Requested path

self.headers

Incoming request headers

self.rfile

Input stream for request data

self.wfile

Output stream for response data

self.send_response()

Sends status code

self.send_header()

Sends response header

self.end_headers()

Finishes response headers

C. The do_GET method

python
def do_GET(self):
This is particularly important.

When Python receives a GET request, BaseHTTPRequestHandler dispatches it to your do_GET() method.

For example:


http
GET / HTTP/1.1
Calls:


python
do_GET()
Your implementation decides what response to return.

D. Preparing the response body

python
message = "Hello from Elenchus"
body = message.encode("utf-8")
Why encode?

Because HTTP response bodies are transmitted as bytes.

Python strings are Unicode text, whereas wfile.write() expects bytes.

E. Sending the response

python
self.send_response(200)
self.send_header("Content-Type", "text/plain; charset=utf-8")
self.send_header("Content-Length", str(len(body)))
self.end_headers()
self.wfile.write(body)
The order matters:

Send the status.

Send the headers.

Finish the headers.

Send the body.

Notice that Content-Length is converted into a string because HTTP headers are textual.

Also, we calculate the length using the encoded bytes, not the original string.

2. Run your server
Start it:


bash
python server.py
Or specify a different port:


bash
python server.py --port 9000
You should see:


text
Elenchus server running on port 8000
3. Test using real curl
Open another terminal.

Test the root endpoint:


bash
curl -i http://localhost:8000/
Expected response:


http
HTTP/1.0 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 19

Hello from Elenchus
Test an unknown path:


bash
curl -i http://localhost:8000/unknown
Expected:


http
HTTP/1.0 404 Not Found
Content-Type: text/plain; charset=utf-8

Not Found
Note: The greeting shown above contains 19 bytes, not 18.

4. Let's see if you understand it
Now that you've seen the complete implementation, let's test your understanding.

Task 1 knowledge check

0/5 answered
1. Why does RequestHandler inherit from BaseHTTPRequestHandler?


To automatically create a database

To reuse Python's HTTP request parsing and handling machinery

To establish a DNS connection

To convert Python into a web framework
2. What happens when a GET request reaches our server?


Python automatically calls do_POST()

HTTPServer calls main() again

BaseHTTPRequestHandler dispatches it to do_GET()

The browser executes do_GET()
3. Why do we call encode('utf-8') on the response message?


To encrypt the message

Because wfile.write() writes bytes, not Python strings

To calculate the HTTP status

To convert text into JSON
4. Why do we use len(body) instead of len(message) for Content-Length?


Because HTTP only accepts integers

Because Content-Length measures the encoded body in bytes

Because strings cannot have lengths

Because it measures the number of headers
5. What does end_headers() do?


Closes the server

Sends the response body

Marks the end of the response headers

Terminates the TCP connection
After the quiz, I want you to explain one thing in your own words:

Why do we call send_response(), send_header() and end_headers() before calling wfile.write()?

If you can explain that without memorizing the code, you're beginning to understand how HTTP responses actually work.


Log in for personalized, step-by-step guidance.


Log in

Sign up for free
is this all about task 1 only?

Yes! Everything we've covered in that implementation belongs to Task 1: Hello (10 points).

However, let's distinguish what Task 1 requires from what we added for good practice.

Task 1 requirements
Requirement

Covered?

Use Python's standard library

Yes

Run an HTTP server

Yes

Configurable port

Yes

Handle GET /

Yes

Return a plain-text greeting

Yes

Correct HTTP status and headers

Yes

What we added beyond the minimum
argparse for command-line configuration.

A 404 Not Found response for unknown paths.

Graceful shutdown using Ctrl+C.

A separate main() function.

These are useful practices, but the advanced HTTP functionality comes in later tasks.

Where we are in the project
Task

Description

Points

0

Setup

10

1

Hello

10

2

List courses

15

3

Single course

15

4

Create course

25

5

Method discipline

10

6

Logging

5

7

README

10

Our current goal is to finish Task 1 properly before moving on.

I suggest you:

Implement the code.

Run it.

Test both endpoints with curl.

Complete the knowledge quiz.

Commit your work.

One important distinction: Task 1 teaches you how to produce an HTTP response. Task 2 will teach you how to produce a structured JSON response.

We'll tackle them separately so you understand each concept rather than just accumulating code.


$ curl localhost:8000
<!DOCTYPE HTML>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <style type="text/css">
            :root {
                color-scheme: light dark;
            }
        </style>
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 501</p>
        <p>Message: Unsupported method ('GET').</p>
        <p>Error code explanation: 501 - Server does not support this operation.</p>
    </body>
</html>

Good, this is a useful debugging exercise. Your server is running, but Python is telling you that it doesn't recognize your GET handler.

The important part is:


text
Error code: 501
Message: Unsupported method ('GET').
What does this mean?
BaseHTTPRequestHandler has a built-in request dispatcher.

When it receives:


http
GET / HTTP/1.1
It looks for a method named:


python
def do_GET(self):
If it cannot find that method, it returns 501 Not Implemented automatically.

Let's investigate
Check these four things in your server.py:

Did you write class RequestHandler(BaseHTTPRequestHandler)?

Is your method named exactly do_GET (capital GET)?

Is do_GET indented inside the RequestHandler class?

Are you running the updated server.py, rather than an older server process?

A common mistake is:


python
class RequestHandler(BaseHTTPRequestHandler):
    pass

def do_GET(self):
    ...
Here, do_GET() is outside the class, so Python's request handler cannot find it.

It must be:


python
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        ...
Your next step
Don't change anything just yet.

Paste your current server.py here.

I'll help you identify exactly where the problem is rather than guessing.


"""
    The servicing file 
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse

class RequestHandler(BaseHTTPRequestHandler):
    """ this class is for the server response. """
    def do_GET(self):
        """ the get method. """
        if self.path == "/":
            message = "Hello from Elenchus"
            body = message.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:
            message = "Not Found"
            body = message.encode("utf-8")

            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)


def main():
    """ main function. """
    parser = argparse.ArgumentParser(
        description="Elenchus HTTP Server"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on"
    )

    args = parser.parse_args()

    server_address = ("", args.port)

    httpd = HTTPServer(server_address, RequestHandler)

    print(f"Elenchus server running on port {args.port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()

I've inspected your code, and I have good news: your implementation is correct. Your do_GET() method is properly named, indented and placed inside RequestHandler.

I don't see a code-level reason for the 501 response.

Let's investigate the likely cause.

1. Most likely: an old server process
You may have an older instance of your server still running on port 8000.

For example:

You started your server before implementing do_GET().

You updated server.py.

The old server process is still running.

Your curl request is reaching that old process.

Python doesn't automatically reload a running server when you edit its source file.

2. Try this
Stop the currently running server using:


bash
Ctrl+C
Then restart it:


bash
python server.py
You should see:


text
Elenchus server running on port 8000
Now test:


bash
curl -i http://localhost:8000/
Expected:


http
HTTP/1.0 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 19

Hello from Elenchus
3. If you still get 501
Check which process owns port 8000:

Linux:


bash
lsof -i :8000
Or:


bash
ss -ltnp | grep 8000
You might discover another Python process listening on that port.

4. A quick code review
Your implementation already demonstrates several good practices:

Correct inheritance.

Correct method naming.

UTF-8 encoding.

Correct byte-based Content-Length.

Appropriate status codes.

Proper response header ordering.

Configurable port.

One small improvement for later: you currently repeat the response-writing logic for both success and error responses. We can refactor that when it becomes useful, but don't worry about it now.

Your next move: Restart the server and run curl -i http://localhost:8000/. Tell me whether you now get 200 OK or still get 501.


the thing was i was running using the short py server.py, but using python3 server.py resolved it

Ah! That makes sense. We've found the issue. 😄

The problem wasn't your implementation; it was the Python interpreter being invoked.

Why did python3 server.py work?
On Linux, these commands aren't necessarily equivalent:


bash
python server.py

bash
python3 server.py
They can point to different Python installations or environments.

For example:

python might point to another interpreter.

python3 might point to your installed Python 3.

Your virtual environment's python should point to the interpreter inside .venv.

Since your project requires Python 3.12+, consistency matters.

My recommendation
Activate your virtual environment:


bash
source .venv/bin/activate
Then check:


bash
which python
python --version
You should see something similar to:


text
/path/to/elenchus-api/.venv/bin/python
Python 3.12.x
Now run:


bash
python server.py
This is preferable because you're explicitly using your project's virtual environment.

Quick knowledge check
Why do you think we create a virtual environment instead of installing all our Python dependencies globally on the computer?

Once you've answered, we'll close Task 1, test your endpoints and commit your implementation.


to have specific tools and versions to use throughout our project, now task 2 but i could not see the headers only saw the greeting message

Exactly right about virtual environments! They isolate your project's Python interpreter and dependencies, helping ensure reproducibility and preventing dependency conflicts with other projects.

Before Task 2, let's address your question about the headers.

1. Why you only saw the greeting
You probably ran:


bash
curl localhost:8000
By default, curl displays the response body, not the response headers.

To see both, use:


bash
curl -i http://localhost:8000/
The -i option tells curl to include the HTTP response headers.

You should see something similar to:


http
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12
Date: ...
Content-Type: text/plain; charset=utf-8
Content-Length: 19

Hello from Elenchus
Other useful curl options:


bash
# Show response headers only
curl -I http://localhost:8000/

# Show verbose request and response information
curl -v http://localhost:8000/
Note: -I sends a HEAD request, not GET. Your current handler doesn't implement HEAD, so it may return 501. We'll address method handling later.

Task 2: List Courses
15 points
Now we're moving from plain-text responses to structured JSON responses.

2. What are we building?
Your API should respond to:


http
GET /courses
With something like:


json
{
    "courses": [
        {
            "id": 1,
            "title": "Python Programming",
            "description": "Learn Python fundamentals",
            "price": 15000,
            "currency": "RWF"
        },
        {
            "id": 2,
            "title": "Web Development",
            "description": "Learn HTML, CSS and JavaScript",
            "price": 20000,
            "currency": "RWF"
        }
    ]
}
You need at least five courses.

You get to decide the resource fields and response structure.

3. New Python concepts
We'll introduce two important things.

A. The json module
Python has a built-in module for converting Python objects into JSON.


python
import json
For example:


python
course = {
    "id": 1,
    "title": "Python Programming",
    "price": 15000
}

response = json.dumps(course)
What happens here?

json.dumps() converts a Python dictionary into a JSON-formatted string.

You can inspect it:


python
print(response)
Output:


json
{"id": 1, "title": "Python Programming", "price": 15000}
Remember the distinction:

Python

JSON

Dictionary

Object

List

Array

None

null

True

true

False

false

B. Content-Type changes
In Task 1, we used:


python
self.send_header("Content-Type", "text/plain; charset=utf-8")
For Task 2, we'll use:


python
self.send_header("Content-Type", "application/json")
Why?

Because we're returning JSON rather than plain text.

4. The implementation
We'll extend your existing server.py.

First, add:


python
import json
Next, define your in-memory courses.

For example, outside your handler class:


python
courses = [
    {
        "id": 1,
        "title": "Python Programming",
        "description": "Learn Python fundamentals",
        "price": 15000,
        "currency": "RWF"
    },
    {
        "id": 2,
        "title": "Web Development",
        "description": "Learn HTML, CSS and JavaScript",
        "price": 20000,
        "currency": "RWF"
    },
    {
        "id": 3,
        "title": "Database Fundamentals",
        "description": "Learn relational databases",
        "price": 18000,
        "currency": "RWF"
    },
    {
        "id": 4,
        "title": "Git and GitHub",
        "description": "Learn version control",
        "price": 10000,
        "currency": "RWF"
    },
    {
        "id": 5,
        "title": "Computer Networks",
        "description": "Understand networking fundamentals",
        "price": 25000,
        "currency": "RWF"
    }
]
Now add another condition to your existing do_GET():


python
elif self.path == "/courses":
    body = json.dumps({
        "courses": courses
    }).encode("utf-8")

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()

    self.wfile.write(body)
Make sure this elif comes before your existing else.

Your request handler now supports:

GET /

GET /courses

404 for other paths.

5. Test your endpoint
Restart your server and run:


bash
curl -i http://localhost:8000/courses
You should receive:

Status 200 OK.

Content-Type application/json.

Content-Length matching the response body size.

Five courses in JSON format.

You can also make the JSON easier to read:


bash
curl -s http://localhost:8000/courses | python3 -m json.tool
6. Knowledge check
Before moving further, I want to test three concepts.

Task 2 mini-quiz

1. What does json.dumps() do?


Converts JSON into a Python dictionary

Converts a Python object into a JSON string

Sends JSON over TCP

Validates an HTTP request

2. Why do we encode the JSON response using UTF-8?


Because HTTP status codes require UTF-8

Because wfile.write() expects bytes

Because JSON cannot contain strings

To encrypt the response

3. Why should we use integer prices instead of floating-point prices?


Integers make HTTP faster

Floating-point arithmetic can introduce precision errors

JSON does not support decimals

Integers are automatically converted into currency


One final challenge: Why do you think we use json.dumps() instead of simply passing our Python dictionary directly to self.wfile.write()?

That's an important distinction between Python data structures and HTTP response bodies.


i created a courses.json file at same level as server.py

Nice! That's a reasonable organizational decision. You're separating your course data from your server logic.

Your project now looks like:


text
elenchus-api/
│
├── .venv/
├── server.py
├── courses.json
├── README.md
└── .gitignore
1. What goes inside courses.json?
Unlike Python dictionaries, JSON uses double quotes for keys and string values.

For example:


json

{
    "courses": [
        {
            "id": 1,
            "title": "Python Programming",
            "description": "Learn Python fundamentals",
            "price": 15000,
            "currency": "RWF"
        },
        {
            "id": 2,
            "title": "Web Development",
            "description": "Learn HTML, CSS and JavaScript",
            "price": 20000,
            "currency": "RWF"
        },
        {
            "id": 3,
            "title": "Database Fundamentals",
            "description": "Learn relational databases",
            "price": 18000,
            "currency": "RWF"
        },
        {
            "id": 4,
            "title": "Git and GitHub",
            "description": "Learn version control",
            "price": 10000,
            "currency": "RWF"
        },
        {
            "id": 5,
            "title": "Computer Networks",
            "description": "Understand networking fundamentals",
            "price": 25000,
            "currency": "RWF"
        }
    ]
}
2. How does Python read this file?
You'll need two things:


python
import json
from pathlib import Path
json understands JSON serialization and deserialization.

Path helps locate files reliably.

For example, to read your file:


python
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "courses.json", "r", encoding="utf-8") as file:
    data = json.load(file)

courses = data["courses"]
Important distinction:

Function

Purpose

json.load()

Reads JSON from a file and converts it into Python objects.

json.loads()

Converts a JSON string into Python objects.

json.dump()

Writes Python objects into a JSON file.

json.dumps()

Converts Python objects into a JSON string.

This is especially important because your API will eventually need to both read and write course data.

3. One architectural consideration
For this project, your assignment explicitly requires in-memory data.

Reading courses.json into a Python list at startup satisfies that requirement, provided you use the in-memory collection while the server runs.

Don't treat the JSON file as a database or automatically write changes back to it.

4. Let me check your understanding
Three questions:

Why would json.load() be more appropriate than json.loads() when reading courses.json?

After loading the file, what Python data type do you expect data["courses"] to be?

If you modify courses in memory, does courses.json automatically change?

Try answering these before we connect your JSON file to GET /courses.