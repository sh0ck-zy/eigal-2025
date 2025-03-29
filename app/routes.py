from flask import Blueprint, jsonify, request, render_template
from app.models.quantities import Quantity
from app import db
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/api/print-types', methods=['GET'])
def get_print_types():
    """Returns unique print types from the database"""
    print_types = db.session.query(Quantity.print_type).distinct().all()
    return jsonify([pt[0] for pt in print_types])

@main.route('/api/waste-calculation', methods=['GET'])
def calculate_waste():
    """Calculate waste based on print type and run quantity"""
    print_type = request.args.get('print_type')
    print_run = request.args.get('print_run', type=int)
    
    if not print_type or not print_run:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Find the most appropriate entry based on print run
    # We'll look for the closest print_run that is less than or equal to the requested amount
    quantity = Quantity.query.filter_by(print_type=print_type) \
        .filter(Quantity.print_run <= print_run) \
        .order_by(Quantity.print_run.desc()) \
        .first()
    
    # If no matching record found with print_run <= requested, get the smallest available
    if not quantity:
        quantity = Quantity.query.filter_by(print_type=print_type) \
            .order_by(Quantity.print_run) \
            .first()
    
    if not quantity:
        return jsonify({'error': 'Print type not found'}), 404
    
    return jsonify(quantity.to_dict())

@main.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')
