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

# Author:
- creih <iherr.9@gmail.com>.
