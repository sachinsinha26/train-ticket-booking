from flask import Blueprint, request, jsonify
from app import app, db
from app.lib.booking import are_seats_booked
from app.lib.seat import (get_available_seats_by_coach_id,
    get_available_seats_by_train_id, get_booked_seats_by_coach_id, get_booked_seats_by_train_id)
from app.lib.const import Error

module = Blueprint('base', __name__)


@module.route('/booking/', methods=['POST'])
def create_booking():
    contents = request.json

    booker_id = contents.get('user_id')
    travel_date = contents.get('travel_date')
    passenger_seat_details = contents.get('passenger_seat_details')

    seat_ids = []
    for passenger_seat_detail in passenger_seat_details:
        seat_id = passenger_seat_detail.get('seat_id')
        seat_ids.append(seat_id)

    if are_seats_booked(seat_ids, travel_date):
        return jsonify(msg="Seats are already booked"), Error.BAD_REQUEST

    return create_booking(booker_id, travel_date, passenger_seat_details)


@module.route('/coach/<int:coach_id>/available-seats/', methods=['GET'])
def get_available_seats_list_by_coach_id(coach_id):
    return jsonify(seats=get_available_seats_by_coach_id(coach_id))


@module.route('/train/<int:train_id>/available-seats/', methods=['GET'])
def get_available_seats_list_by_train_id(train_id):
    return jsonify(seats=get_available_seats_by_train_id(train_id))


@module.route('/coach/<int:coach_id>/booked-seats/', methods=['GET'])
def get_booked_seats_list_by_coach_id(coach_id):
    return jsonify(seats=get_booked_seats_by_coach_id(coach_id))


@module.route('/train/<int:train_id>/booked-seats/', methods=['GET'])
def get_booked_seats_list_by_train_id(train_id):
    return jsonify(seats=get_booked_seats_by_train_id(train_id))


app.register_blueprint(module)
