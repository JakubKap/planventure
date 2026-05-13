from datetime import datetime
from typing import Any, Dict, List

from flask import Blueprint, jsonify, request

from auth_middleware import require_auth, get_current_user
from extensions import db
from itinerary import generate_itinerary_template, quick_itinerary_template
from models import Trip

trips_bp = Blueprint('trips', __name__)


@trips_bp.route('', methods=['GET'])
@require_auth
def get_trips():
    """Get all trips for the authenticated user."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    trips = Trip.query.filter_by(user_id=user.id).all()
    return jsonify({
        'trips': [trip.to_dict() for trip in trips],
        'count': len(trips)
    }), 200


@trips_bp.route('/<int:trip_id>', methods=['GET'])
@require_auth
def get_trip(trip_id: int):
    """Get a specific trip by ID."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404

    return jsonify({'trip': trip.to_dict()}), 200


@trips_bp.route('', methods=['POST'])
@require_auth
def create_trip():
    """Create a new trip for the authenticated user."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    payload = request.get_json(silent=True) or {}

    # Validate required fields
    required_fields = ['destination', 'start_date', 'end_date']
    missing_fields = [field for field in required_fields if not payload.get(field)]

    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing_fields)}',
            'fields': missing_fields
        }), 400

    destination = payload.get('destination', '').strip()
    coordinates = payload.get('coordinates', '').strip()
    itinerary = payload.get('itinerary', '')
    auto_generate_itinerary = payload.get('auto_generate_itinerary', False)

    # Validate destination
    if not destination:
        return jsonify({'error': 'Destination cannot be empty.'}), 400

    # Parse and validate dates
    try:
        start_date = datetime.fromisoformat(payload['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(payload['end_date'].replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return jsonify({
            'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).'
        }), 400

    # Validate date logic
    if end_date <= start_date:
        return jsonify({'error': 'End date must be after start date.'}), 400

    # Auto-generate itinerary if requested and not provided
    if auto_generate_itinerary and not itinerary:
        itinerary = generate_itinerary_template(
            destination,
            payload['start_date'],
            payload['end_date']
        )

    # Create trip
    trip = Trip(
        user_id=user.id,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        coordinates=coordinates if coordinates else None,
        itinerary=itinerary if itinerary else None
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify({'trip': trip.to_dict()}), 201


@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@require_auth
def update_trip(trip_id: int):
    """Update an existing trip."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404

    payload = request.get_json(silent=True) or {}

    # Update fields if provided
    if 'destination' in payload:
        destination = payload['destination'].strip()
        if not destination:
            return jsonify({'error': 'Destination cannot be empty.'}), 400
        trip.destination = destination

    if 'coordinates' in payload:
        trip.coordinates = payload['coordinates'].strip() or None

    if 'itinerary' in payload:
        trip.itinerary = payload['itinerary'] or None

    # Handle date updates
    start_date = None
    end_date = None

    if 'start_date' in payload:
        try:
            start_date = datetime.fromisoformat(payload['start_date'].replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid start_date format.'}), 400

    if 'end_date' in payload:
        try:
            end_date = datetime.fromisoformat(payload['end_date'].replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid end_date format.'}), 400

    # Use existing dates if not provided
    start_date = start_date or trip.start_date
    end_date = end_date or trip.end_date

    # Validate date logic
    if end_date <= start_date:
        return jsonify({'error': 'End date must be after start date.'}), 400

    trip.start_date = start_date
    trip.end_date = end_date

    db.session.commit()

    return jsonify({'trip': trip.to_dict()}), 200


@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@require_auth
def delete_trip(trip_id: int):
    """Delete a trip."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404

    db.session.delete(trip)
    db.session.commit()

    return jsonify({'message': 'Trip deleted successfully.'}), 200