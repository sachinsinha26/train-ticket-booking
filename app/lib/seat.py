from flask import jsonify

from app import db
from app.lib.const import Error
from app.models import Coach, Seat, SeatBooking


def add_seats(coach):
    coach_counts = Coach.SeatsCount.AC_Sleeper

    if coach.type == Coach.Type.Seater:
        coach_counts = Coach.SeatsCount.Seater
    if coach.type == Coach.Type.Non_AC_Sleeper:
        coach_counts = Coach.SeatsCount.Non_AC_Sleeper

    for seat_number in range(1, coach_counts + 1):
        seat = Seat(seat_number, coach.id)
        db.session.add(seat)

    db.session.commit()


def delete_seats(coach_id):
    seat_bookings = (
        db.session.query(SeatBooking)
        .join(Seat, Seat.id == SeatBooking.seat_id)
        .filter(Seat.coach_id == coach_id)
        .all()
    )

    if seat_bookings is not None:
        return jsonify(msg="Seats are booked in this coach"), Error.BAD_REQUEST

    db.session.query(Seat).filter(Seat.coach_id).delete()
    db.session.commit()

    return jsonify()

def get_seats_by_coach_id(coach_id):
    seats_list = (
        db.session.query(Seat, SeatBooking)
        .outerjoin(SeatBooking, Seat.id == SeatBooking.seat_id)
        .filter(Seat.coach_id == coach_id)
        .all()
    )

    seats = []
    for seat, booking in seats_list:
        seat = seat.serialize
        seat.update({'status': 'booked' if booking is not None else 'vacant'})
        seats.append(seat)

    return seats

def get_seats_by_train_id(train_id):
    seats_list = (
        db.session.query(Seat, SeatBooking)
        .join(Coach, Coach.id == Seat.coach_id)
        .outerjoin(SeatBooking, Seat.id == SeatBooking.seat_id)
        .filter(Coach.train_id == train_id)
        .all()
    )

    seats = []
    for seat, booking in seats_list:
        seat = seat.serialize
        seat.update({'status': 'booked' if booking is not None else 'vacant'})
        seats.append(seat)

    return seats


def get_available_seats_by_coach_id(coach_id):
    seats = (
        db.session.query(Seat)
        .outerjoin(SeatBooking, Seat.id == SeatBooking.seat_id)
        .filter(
            Seat.coach_id == coach_id,
            SeatBooking.id == None
        )
        .all()
    )

    return [seat.serialize for seat, in seats]


def get_available_seats_by_train_id(train_id):
    seats = (
        db.session.query(Seat)
        .join(Coach, Coach.id == Seat.coach_id)
        .outerjoin(SeatBooking, Seat.id == SeatBooking.seat_id)
        .filter(
            Coach.train_id == train_id,
            SeatBooking.id == None
        )
        .all()
    )

    return [seat.serialize for seat, in seats]


def get_booked_seats_by_coach_id(coach_id):
    seats = (
        db.session.query(Seat)
        .join(SeatBooking, Seat.id == SeatBooking.seat_id)
        .filter(Seat.coach_id == coach_id)
        .all()
    )

    return [seat.serialize for seat, in seats]


def get_booked_seats_by_train_id(train_id):
    seats = (
        db.session.query(Seat)
        .join(Coach, Coach.id == Seat.coach_id)
        .join(SeatBooking, Seat.id == SeatBooking.seat_id)
        .filter(Coach.train_id == train_id)
        .all()
    )

    return [seat.serialize for seat, in seats]
