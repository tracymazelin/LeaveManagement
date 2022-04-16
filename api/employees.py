from api import bp
from flask import jsonify
from models import Employee
import json

@bp.route('/employee/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_employee(id):
    return jsonify(Employee.query.get_or_404(id).to_dict())


@bp.route('/employees', methods=['GET'])
#@token_auth.login_required
def get_employees():
    return jsonify(Employee.to_collection_dict())

