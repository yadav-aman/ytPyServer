# Backend Assignment

## Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## How to run the app

### Running server -

> For this python>= 3.8 is required

## Open a terminal and run the following commands

- ### Setting-up virtual environment

  ```bash
  $ pip3 install virtualenv
  $ virtualenv venev
  $ source ./venv/bin/activate
  ```

- ### Installing Dependencies
  ```bash
  $ cd server
  $ pip install -r requirements.txt
  ```
- ### Setting up environment secret key (for encryption)

  ```
  $ touch env.py
  ```

  > Copy the API-keys inside **env.py** file, in the same format as given in **env.example.py file**

- ### Starting the server

  ```
  $ cd ..
  $ python3 server/main.py
  ```

- Now, the server is hosted at localhost:8000, and the API documentation along with all the endpoints can be accessed at [localhost:8000/docs](http://localhost:8000/docs)

## Features Implemented

- [x] RESTAPI
- [x] Fetch Youtube API every 60 seconds to retrive latest vidoes
- [x] Support multiple api key in case of Quota exceed
- [x] Sort results based on time and title
