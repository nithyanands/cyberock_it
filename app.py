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

# Ensure Assigned_to field is optional and if not provided, default to "L1 Ops Team"
    allowed_assignees = ["Security Team", "Infrastructure Team", "Frontend Team", "Backend Team", "L1 Ops Team", "Network Ops"]
    assigned_to = ticket_data.get("assigned_to") or "L1 Ops Team"
    if assigned_to not in allowed_assignees:
        return jsonify({"error": f"Invalid assigned_to '{assigned_to}'. Should be one of: {', '.join(allowed_assignees)}"}), 400

    new_ticket = {
        "ticket_id": next_id,
        "title": ticket_data.get("title"),
        "description": ticket_data.get("description"),
        "severity": severity,
        "status": "open",
        "date_reported": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reported_by": ticket_data.get("reported_by"),
        "assigned_to": assigned_to,
        "closed_date": None
    }
    tickets.append(new_ticket)
    next_id += 1
    return jsonify(new_ticket), 201

# get all tickets

@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    results = tickets
# Enable search functionality for title and description fields
    search = request.args.get('search')
    if search:
        filtered_results = []
        for t in results:
            title_match = search.lower() in t["title"].lower()
            description_match = search.lower() in t["description"].lower()
            if title_match or description_match:
                filtered_results.append(t)
        results = filtered_results
        
# Enable filtering with severity if provided in input url
    severity_filter = request.args.get('severity')
    if severity_filter:
        filtered_results = []
        for t in results:
            if t['severity'] == severity_filter:
                filtered_results.append(t)
        results = filtered_results

# Enable filtering with status if provided in input url
    status_filter = request.args.get('status')
    if status_filter:
        filtered_results = []
        for t in results:
            if t['status'] == status_filter:
                filtered_results.append(t)
        results = filtered_results

# Enable sorting by severity, status, date_reported, or ticket_id if provided in input url

    sort_by = request.args.get('sort')
    if sort_by in ['severity', 'status', 'date_reported', 'ticket_id']:
        def get_sort_value(ticket):
            return ticket[sort_by]
        results = sorted(results, key=get_sort_value)

    return jsonify(results), 200

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
    allowed_assignees = ["Security Team", "Infrastructure Team", "Frontend Team", "Backend Team", "L1 Ops Team", "Network Ops"]
    
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            
            # Severity validation if provided in the update request
            if "severity" in ticket_data:
                new_severity = ticket_data.get("severity")
                if new_severity not in allowed_severities:
                    return jsonify({"error": f"Invalid severity '{new_severity}'. Should be one of: {', '.join(allowed_severities)}"}), 400
                ticket["severity"] = new_severity
            
            # Assigned_to validation if provided in the update request
            if "assigned_to" in ticket_data:
                new_assignee = ticket_data.get("assigned_to")
                if new_assignee not in allowed_assignees:
                    return jsonify({"error": f"Invalid assigned_to '{new_assignee}'. Should be one of: {', '.join(allowed_assignees)}"}), 400
                ticket["assigned_to"] = new_assignee
                                      
            # Status validation if provided in the update request
            
            if "status" in ticket_data:
                new_status = ticket_data.get("status")
                if new_status not in allowed_statuses:                
                    return jsonify({"error": f"Invalid status '{new_status}'. Should be one of: {', '.join(allowed_statuses)}"}), 400
                ticket["status"] = new_status
                
                #When status is updated to "Resolved", set the closed_date to the current date and time
                if new_status == "Resolved":
                    ticket["closed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    ticket["closed_date"] = None
            
                        
            ticket["title"] = ticket_data.get("title", ticket["title"])
            ticket["description"] = ticket_data.get("description", ticket["description"])
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

#summary of tickets by severity, status

@app.route('/report/summary', methods=['GET'])
def get_summary():
    severity_summary = {}
    status_summary = {}
    for ticket in tickets:
        severity = ticket["severity"]
        severity_summary[severity] = severity_summary.get(severity, 0) + 1
        
        status = ticket["status"]
        status_summary[status] = status_summary.get(status, 0) + 1
    summary = {
        "total_tickets": len(tickets),
        "severity_summary": severity_summary,
        "status_summary": status_summary
    }
    return jsonify(summary), 200
    
if __name__ == '__main__':
    app.run(debug=True)