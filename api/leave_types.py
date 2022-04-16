from api import bp
from flask import jsonify
from models import LeaveType
import json


@bp.route('/leave_type/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_leave_type(id):
    return jsonify(LeaveType.query.get_or_404(id).to_dict())


@bp.route('/leave_types', methods=['GET'])
#@token_auth.login_required
def get_leave_types():
    return jsonify(LeaveType.to_collection_dict())

    
