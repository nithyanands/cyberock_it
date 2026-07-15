# cyberock_it
Issues &amp; Vulnerabilities Tracking System Adv Programming CA2

A REST API backend for tracking security issues and vulnerability for the company **Cyberock**

## Project Overview:
This system performs Create, Read, Update, Delete (CRUD) operations of the issues and vulnerability records.
Built using python, flask and tested using postman

## Tools & Software stack:
- Language: Python 3.14
- Framework: Flask
- Testing: Postman
- Version control: GitHUb / Git

## Data requirements:
Each Ticket includes following fields,
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
1. Clone this repository in local machine
2. create virtual environment (venv)
3. Activate venv
4. Install flask and dependencies
5. Run the flask application
6. Web Application is up and running at http://127.0.0.1:5000

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Application status |
| POST | /tickets | Creates a new ticket |
| GET | /tickets | List all tickets , supports search, filter and sort using query parameters | |
| GET | /tickets/<ticket_id> | Get a single ticket by ID |
| PUT | /tickets/<ticket_id> | Updates an existing ticket |
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
- Update - PUT /tickets/<id>, updates only fields sent in the request and allowed values from severities,status,assignees
- Delete - DELETE /tickets/<id>
- Search - GET /tickets?search=, enables search title and description fields
- Filtering - GET /tickets?severity= and ?status=, Enables filtering with severity and status along with search
- Sorting - GET /tickets?sort=, Enables sorting by severity, status, date_reported, or ticket_id
- Reporting - GET /report/summary, gives total tickets and severity/status counts
- Validation - severity, status and assigned_to only accept values from a allowed values, invalid inputs are returned with error messages.
- Integrity - ticket_id comes from the server so no duplicates possible, status can only change through update, close_date is set automatically when resolved and cleared if reopened

## Testing
Tested all the endpoints manually using Postman, checking both valid requests and error cases.

Testing covered:
- All endpoint - application status and error cases (missing fields, input values not in the allowed list, ticket not found in the list and dictionary)
- Edge cases like empty strings and whitespace-only input for required fields and severity
- closed_date updated and cleared both ways - setting a ticket to Resolved and then reopening it
- Query parameter on GET /tickets (search, severity, status, sort) tested each one at a time and combined together
- Validated /report/summary for total number of tickets from the actual ticket list based on severity and status

## Code Attribution Summary
- Usage of Basic flask and python syntax (routes, request handling, jsonify, loops, if conditions, lists/dictionaries) follows standard flask documentation, not attributed individually.

- The business rules used (severity levels, status workflow, close_date tied to resolution, team based assignment) in the scope come from my own work experience in Fault Management, Change Management and Configuration Management using ITSM and BMC Remedy. 

- I have created a simplified system that does basic required functionality with validation and integrity rules compared to the real world systems which have complex rules and role based access and customized feature that supports customer requirements.

- `app.config['JSON_SORT_KEYS']` was tried first and had no effect. Checked Flask's official documentation (https://flask.palletsprojects.com/en/stable/config/), which confirmed this config key was removed in Flask 2.3+, replaced by `app.json.sort_keys`. Used the documented replacement instead of guessing further, hence marked as **online resource** rather than **self** for this specific fix.