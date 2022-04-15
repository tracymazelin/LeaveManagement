from flask import jsonify, request, url_for, abort, Blueprint
from app import db
from models import Employee

#from app.api.auth import token_auth
#from app.api.errors import bad_request
api = Blueprint('api', __name__)

@api.route('/employees/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_employee(id):
    data = Employee.get_logged_in_employee_id(id)
    return jsonify(data)