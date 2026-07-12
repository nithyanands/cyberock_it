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
    
# Ensure all required fields available in the ticket creation request

    required_fields = ["title", "description", "reported_by"]
    missing_fields = []
    for field in required_fields:
        if not ticket_data.get(field):
            missing_fields.append(field)
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

# Ensure Severity input has to be one of the allowed values

    allowed_severities = ["Low", "Medium", "High", "Critical"]
    severity = ticket_data.get("severity", "Medium")
    if severity not in allowed_severities:
        return jsonify({"error": f"Invalid severity '{severity}'. Should be one of: {', '.join(allowed_severities)}"}), 400

 
    
    new_ticket = {
        "ticket_id": next_id,
        "title": ticket_data.get("title"),
        "description": ticket_data.get("description"),
        "severity": severity,
        "status": "open",
        "date_reported": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reported_by": ticket_data.get("reported_by"),
        "assigned_to": ticket_data.get("assigned_to" , "L1 Ops Team"),
        "closed_date": None
    }
    tickets.append(new_ticket)
    next_id += 1
    return jsonify(new_ticket), 201

# get all tickets

@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    return jsonify(tickets), 200

# get a specific ticket by ID

@app.route('/tickets/<int:ticket_id>',methods=['GET'])
def get_specific_ticket(ticket_id):
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return jsonify(ticket), 200
    return jsonify({"error": "Ticket not found"}), 404

# update a specific ticket by ID

@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket_data = request.get_json()
    allowed_statuses = ["open", "In Progress", "Resolved"]
    allowed_severities = ["Low", "Medium", "High", "Critical"]
    
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            
            # Severity validation if provided in the update request
            if "severity" in ticket_data:
                new_severity = ticket_data.get("severity")
                if new_severity not in allowed_severities:
                    return jsonify({"error": f"Invalid severity '{new_severity}'. Should be one of: {', '.join(allowed_severities)}"}), 400
                ticket["severity"] = new_severity
            
            # Status validation if provided in the update request
            
            if "status" in ticket_data:
                new_status = ticket_data.get("status")
                if new_status not in allowed_statuses:                
                    return jsonify({"error": f"Invalid status '{new_status}'. Should be one of: {', '.join(allowed_statuses)}"}), 400
                ticket["status"] = new_status
                
            
            ticket["title"] = ticket_data.get("title", ticket["title"])
            ticket["description"] = ticket_data.get("description", ticket["description"])
            ticket["assigned_to"] = ticket_data.get("assigned_to", ticket["assigned_to"])
            return jsonify(ticket), 200
    return jsonify({"error": "Ticket not found"}), 404

# Delete a specific ticket by ID
@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            tickets.remove(ticket)
            return jsonify({"message": f"Ticket {ticket_id} deleted successfully"}), 200
    return jsonify({"error": "Ticket not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)