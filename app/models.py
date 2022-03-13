from sqlalchemy.dialects.mysql import TINYINT, BIGINT, TIMESTAMP, INTEGER

from app import db


class Train(db.Model):
    id = db.Column(BIGINT(20), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    time_created = db.Column(TIMESTAMP, server_default=db.func.now())

    # source, destination, stops, timings, days of travel of train are ignored currently.

    def __init__(self, name):
        self.name = name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Coach(db.Model):
    class Type:
        AC_Sleeper = "ac_sleeper"
        Non_AC_Sleeper = "non_ac_sleeper"
        Seater = "seater"

    class SeatsCount:
        AC_Sleeper = 60
        Non_AC_Sleeper = 60
        Seater = 120

    allowed_types = [Type.AC_Sleeper, Type.Non_AC_Sleeper, Type.Seater]

    id = db.Column(BIGINT(20), primary_key=True)
    train_id = db.Column(BIGINT(20), db.ForeignKey('train.id'))
    type = db.Column(db.String(50))
    time_created = db.Column(TIMESTAMP, server_default=db.func.now())

    def __init__(self, train_id, type_):
        self.train_id = train_id
        self.type = type_

    @property
    def serialize(self):
        return {
            'id': self.id,
            'train_id': self.train_id,
            'type': self.type
        }


class Seat(db.Model):
    id = db.Column(BIGINT(20), primary_key=True)
    seat_number = db.Column(BIGINT(20))
    coach_id = db.Column(BIGINT(20), db.ForeignKey('coach.id'))

    # seat type like lower, middle are ignored.

    def __init__(self, seat_number, coach_id):
        self.seat_number = seat_number
        self.coach_id = coach_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'coach_id': self.coach_id,
            'seat_number': self.seat_number
        }


class User(db.Model):
    class FlagsBit:
        ADMIN_BIT = 1

    id = db.Column(BIGINT(20), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    flags = db.Column(BIGINT(20), nullable=False, default=0)
    time_created = db.Column(TIMESTAMP, server_default=db.func.now())

    def __init__(self, email, name):
        self.email = email
        self.name = name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }

class Booking(db.Model):
    id = db.Column(BIGINT(20), primary_key=True)
    booker_id = db.Column(BIGINT(20), db.ForeignKey('user.id'))
    travel_date = db.Column(db.String(20))  # haven't added validation for dates.
    time_created = db.Column(TIMESTAMP, server_default=db.func.now())
    time_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # booking amount etc are ignored

    def __init__(self, booker_id, travel_date):
        self.booker_id = booker_id
        self.travel_date = travel_date

    @property
    def serialize(self):
        return {
            'id': self.id,
            'booker_id': self.booker_id,
            'travel_date': self.travel_date,
            'time_created': self.time_created,
            'time_updated': self.time_updated
        }


class SeatBooking(db.Model):
    id = db.Column(BIGINT(20), primary_key=True)
    traveller_name = db.Column(db.String(50))
    traveller_age = db.Column(INTEGER)
    seat_id = db.Column(BIGINT(20), db.ForeignKey('seat.id'))
    booking_id = db.Column(BIGINT(20), db.ForeignKey('booking.id'))

    def __init__(self, traveller_name, traveller_age, seat_id, booking_id):
        self.seat_id = seat_id
        self.booking_id = booking_id
        self.traveller_age = traveller_age
        self.traveller_name = traveller_name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'seat_id': self.seat_id,
            'booking_id': self.booking_id,
            'traveller_age': self.traveller_age,
            'traveller_name': self.traveller_name
        }
