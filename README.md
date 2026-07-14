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

## Setup instructions:
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
| GET | /tickets | List all tickets , supports search, filter and sort using query parameters | |
| GET | /tickets/<ticket_id> | Get a single ticket by ID |
| PUT | /tickets/<ticket_id> | Update an existing ticket |
| DELETE | /tickets/<ticket_id> | Delete a ticket by ID |
| GET | /report/summary | Get summary of ticket count by severity and status |

## GET /tickets query parameters
- search - enable search function using title and description
- severity - enable filter function by severity value
- status - enable filter function by status value
- sort - enable sorting by severity, status, date_reported, or ticket_id

All the above options can be used together in the same request, example:
`GET /tickets?search=team&severity=High&status=open&sort=date_reported`

## Requirements coverage
- Entry - POST /tickets, checks the following required fields are given: title, description, reported_by
- Read - GET /tickets and GET /tickets/<id>
- Update - PUT /tickets/<id>, only fields sent in the request and allowed values from severities,status,assignees
- Delete - DELETE /tickets/<id>
- Search - GET /tickets?search=, enables search title and description fields
- Filtering - GET /tickets?severity= and ?status=, Enables filtering with severity and status, combined with search
- Sorting - GET /tickets?sort=, Enables sorting by severity, status, date_reported, or ticket_id
- Reporting - GET /report/summary, gives total tickets and severity/status counts
- Validation - severity, status and assigned_to only accept values from a allowed values, invalid inputs are returned with error messages.
- Integrity - ticket_id comes from the server so no duplicates possible, status can only change through update, close_date is set automatically when resolved and cleared if reopened