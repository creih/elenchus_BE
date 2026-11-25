## Project 0x00: The Raw Server (elenchus)

# Repo Description.
This will serve as the backend repo to my elenchus project that is meant to be a kind of e-learning platform designed to make me comprehend and understand core logics, concepts and principles of SWE especially in the Web development niche.

# Pre-requisites
- python3.
- virtual environment( venv).

# Installation
- clone the repo from github `git@github.com:creih/elenchus_BE.git`.
- setup your own virtual environment.
- no requirements.txt file yet for dependencies so no need for the freeze cmd.

# Running the http server
- running the server `python3 -m http.server`.
- for testing the endpoints use `curl localhost:{port-number}` port number could be 8000 or else if you choose.

# Decision: repo layout.
- With the use of python for the backend and typescript coupled with react as our frontend foundation I've opted for using 2 repos one for the frontend(Elenchus_FE) and the backend side of it( Elenchus_BE). This choice was made in conjuction with my thoughts of deployment setups and configuration settings for when we get to that part as most hosting services I know prefer keeping backend and frontend deployments seperate.
- The changes in backend will not affect the fontend repo in this poly-repo style i chose as the 2 repos will only interact via the APIs contracts.
- Now this is highly efficient for teams of different developers as it would provide some form of separation of powers and responsibilities, whereas for one person it will be more complicate to manage but most beneficial as this is how i think industries do things at the pro stage.
- the cheapest of the 2 is poly repo as if some day i decide to implement a c/c++ or c# backend i'll have to only delink the url my frontend was using to acquire the backend logics and vice versa if i ever need to run another frontend i'll only have to start working on that frontend without worrying about separating our backend logic from ourfrontend UI. 
- for each repo there will be a notes/ explaining the read materials with regards to their relevancy if the material talked about backend things and concepts it will be found in the backend repo in the notes folder that will be located amongst the root folders of the repo, that goes for the README.md files too they will only contain details discussed in projects that relate to their repos.

# Endpoint descriptions:
- GET / -> this endpoint returns a greeting string and appropriate headers
```
$ curl -i -X GET http://localhost:8000/
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.14.7
Date: Tue, 24 Nov 2026 07:12:30 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 19

Hello from Elenchus
```
- GET /courses  -> here we return a list of 5 courses registered in a file that is passed to variable memory
```
$ curl -X GET http://localhost:8000/courses | python3 -m json.tool
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100    624 100    624   0      0   2628      0                              0
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
```  
- GET /courses/:id -> here the endpoint specifically returns a single specific course using its id
```
$ curl -X GET http://localhost:8000/courses/3 | python3 -m json.tool
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100    123 100    123   0      0    459      0                              0
{
    "id": 3,
    "title": "Database Fundamentals",
    "description": "Learn relational databases",
    "price": 18000,
    "currency": "RWF"
}
```
- POST /course  -> creating new course and new id generation depending on max id in memory
```
$ curl -i -X POST http://localhost:8000/courses -H "Content-Type: application/json" -d '{"title":"ML & AI", "descrip
tion":"Learn ML & AI","price":16000,"currency":"RWF"}'
HTTP/1.0 201 Created
Server: BaseHTTP/0.6 Python/3.14.7
Date: Tue, 24 Nov 2026 07:22:56 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 96
Location: /courses/6

{"id": 6, "title": "ML & AI", "description": "Learn ML & AI", "price": 16000, "currency": "RWF"}
```
- Method discipline     -> unsupported paths and methods
- Logs  -> logging activities, status, methods and duration
```
2026-11-24 09:12:30,413 INFO GET / 200 0.21ms
2026-11-24 09:15:23,553 INFO GET /courses 200 0.21ms
2026-11-24 09:15:44,966 INFO GET /courses 200 17.60ms
2026-11-24 09:15:47,899 INFO GET /courses 200 16.30ms
2026-11-24 09:16:04,510 INFO GET /courses 200 10.06ms
2026-11-24 09:17:29,158 INFO GET /courses/3 200 46.09ms
2026-11-24 09:22:56,379 INFO POST /courses 201 0.24ms
```
- graceful server shutdown on ctrl+c (also implemented but not sure how to display it hopefully this is enough)
```
Elenchus server running on port 8000

Shutting down server...
```


# Learning objectives
- In the http request travels headers like content-type, content-length, status and request body, while in the response the server changes the request body for response body.
- http is stateless because the server doesn't record past request solving issues that would slow down responses or jam them like load balancing bottlenecks amongst others.
- methods tells the server what actio to do on a certain path using the data in the body of the request and status comfirms whether that action succeeded or failed.
- server knows the end of the body through using content-length specified into the headeed of the request.
- because decimals because base ten fractions can not be well represented in binary

# Author:
- creih <iherr.9@gmail.com>.
