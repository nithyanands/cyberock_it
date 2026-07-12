# cyberock_it
Issue &amp; Vulnerability Tracking System Adv Programming CA2

A REST API backend for tracking security issues and vulnerability for the company **Cyberock**

## Project Overview:
The system performs Create, Read, Update, Delete (CRUD) operations of the issues and vulnerability records.
Built using python, flask and tested using postman

## Tools & Software stack:
- Language: Python 3.14
- Framework: Flask
- Testing: Postman
- Version control: GitHUb / Git

## Data requirements:
Each Ticket contains following fields,
- ticket_id - automatically assigned number
- title - Issue heading
- description - issue details
- severity - Low / Medium / High / Critical
- status - Open / In progress / Resolved
- date_reported - date and time of the ticket creation
- reported_by - Reported username
- assigned_to - Ticket ownership
- close_date - issue resolved date

## Setup instrcutions:
1. Clone this repo in local machine
2. create virtual environment (venv)
3. Activate venv
4. Install flask and dependencies
5. Run the flask app
6. Web Application is up and running at http://127.0.0.1:5000

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Application status |
| POST | /tickets | Create a new ticket |
| GET | /tickets | List all tickets |
| GET | /tickets/<ticket_id> | Get a single ticket by ID |


