from flask import Flask, jsonify, request
from datetime import datetime
app = Flask(__name__)
# In-memory storage for tickets
tickets = []
next_id = 1

# Test route to check if the API is running and accessible on web and postman

@app.route('/')
def home():
    return {"message": "Cyberock Issue Tracker API is test running"}

# Create a new ticket record from Postman request body

@app.route('/tickets' , methods=['POST'])
def create_ticket():
    global next_id
    ticket_data = request.get_json()
    new_ticket = {
        "ticket_id": next_id,
        "title": ticket_data.get("title"),
        "description": ticket_data.get("description"),
        "severity": ticket_data.get("severity"),
        "status": ticket_data.get("status", "open"),
        "date_reported": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reported_by": ticket_data.get("reported_by"),
        "assigned_to": ticket_data.get("assigned_to"),
        "closed_date": None
    }
    tickets.append(new_ticket)
    next_id += 1
    return jsonify(new_ticket), 201

# get all tickets
@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    return jsonify(tickets), 200


if __name__ == '__main__':
    app.run(debug=True)