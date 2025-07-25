from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
api = Api(app)

issues = []
issue_id_counter = 1
VALID_STATUSES = {"open", "closed"}

def validate_status(status):
    return status.lower() in VALID_STATUSES

class IssueListResource(Resource):
    def get(self):
        return {"issues": issues}, 200

    def post(self):
        global issue_id_counter
        data = request.get_json()

        if not data or 'title' not in data or 'description' not in data or 'status' not in data:
            raise BadRequest("Fields 'title', 'description', and 'status' are required.")

        if not validate_status(data['status']):
            raise BadRequest("Status must be 'open' or 'closed'.")

        issue = {
            'id': issue_id_counter,
            'title': data['title'],
            'description': data['description'],
            'status': data['status'].lower()
        }
        issues.append(issue)
        issue_id_counter += 1
        return {"message": "Issue reported successfully", "issue": issue}, 201

class IssueResource(Resource):
    def get(self, id):
        issue = next((i for i in issues if i['id'] == id), None)
        if not issue:
            raise NotFound("Issue not found.")
        return issue, 200

    def put(self, id):
        data = request.get_json()
        issue = next((i for i in issues if i['id'] == id), None)
        if not issue:
            raise NotFound("Issue not found.")

        if 'title' in data:
            issue['title'] = data['title']
        if 'description' in data:
            issue['description'] = data['description']
        if 'status' in data:
            if not validate_status(data['status']):
                raise BadRequest("Status must be 'open' or 'closed'.")
            issue['status'] = data['status'].lower()

        return {"message": "Issue updated successfully", "issue": issue}, 200

    def delete(self, id):
        global issues
        issue = next((i for i in issues if i['id'] == id), None)
        if not issue:
            raise NotFound("Issue not found.")

        issues = [i for i in issues if i['id'] != id]
        return {"message": f"Issue {id} deleted successfully."}, 200

# Register routes
api.add_resource(IssueListResource, '/issues')
api.add_resource(IssueResource, '/issues/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
