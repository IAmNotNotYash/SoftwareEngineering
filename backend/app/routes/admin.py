from flask import Blueprint, jsonify

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/health', methods=['GET'])
def admin_health():
    return jsonify({"status": "admin module is up"}), 200
