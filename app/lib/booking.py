from flask import jsonify

from app import db
from app.models import SeatBooking, Booking


def are_seats_booked(seats, travel_date):
    seats_booked = (
        db.session.query(SeatBooking)
        .join(Booking, Booking.id == SeatBooking.booking_id)
        .filter(
            SeatBooking.seat_id.in_(seats),
            Booking.travel_date == travel_date
        )
        .all()
    )

    return True if seats_booked else False


def create_booking(booker_id, travel_date, passenger_seat_details):
    booking = Booking(booker_id, travel_date)
    db.session.add(booking)
    db.session.commit(booking)

    seat_bookings = []
    for passenger_seat_detail in passenger_seat_details:
        seat_id = passenger_seat_detail.get('seat_id')
        traveller_age = passenger_seat_detail.get('traveller_age')
        traveller_name = passenger_seat_detail.get('traveller_name')

        seat_booking = SeatBooking(
            traveller_name,
            traveller_age,
            seat_id,
            booking.id
        )
        db.session.add(seat_booking)
        db.session.commit(seat_booking)

        seat_bookings.append(seat_booking.serialize)

    return jsonify(booking=booking.serialize, seat_bookings=seat_bookings)

