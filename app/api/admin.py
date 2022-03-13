from flask import Blueprint, request, jsonify
from app import app, db
from app.lib import user
from app.lib.seat import add_seats, get_seats_by_coach_id, get_seats_by_train_id
from app.models import Train, Coach
from app.lib.const import Error

module = Blueprint('admin', __name__)


@module.route('/train/', methods=['POST'])
def add_train():
    contents = request.json

    if user.is_admin(contents.get('user_id')):
        return jsonify(), Error.PERMISSION_DENIED

    if not contents.get('name'):
        return jsonify(), Error.BAD_REQUEST

    train_name = contents['name']
    train = Train(train_name)
    db.session.add(train)
    db.session.commit()

    return jsonify(train=train.serialize)


@module.route('/coach/', methods=['POST'])
def add_coach():
    contents = request.json

    if user.is_admin(contents.get('user_id')):
        return jsonify(), Error.PERMISSION_DENIED

    if (
        not contents.get('train_id')
        or not contents.get('type')
        or contents.get('type') not in Coach.allowed_types
    ):
        return jsonify(), Error.BAD_REQUEST

    coach = Coach(contents.get('train_id'), contents.get('type'))
    db.session.add(coach)
    db.session.commit()

    add_seats(coach)

    return jsonify(coach=coach.serialize)

@module.route('/coach/', methods=['DELETE'])
def delete_coach():
    contents = request.json

    if user.is_admin(contents.get('user_id')):
        return jsonify(), Error.PERMISSION_DENIED

    if not contents.get('coach_id'):
        return jsonify(), Error.BAD_REQUEST

    return delete_coach(contents.get('coach_id'))


@module.route('/coach/<int:coach_id>/seats/', methods=['GET'])
def get_seats_list_by_coach_id(coach_id):
    contents = request.json

    if user.is_admin(contents.get('user_id')):
        return jsonify(), Error.PERMISSION_DENIED

    return jsonify(seats=get_seats_by_coach_id(coach_id))


@module.route('/train/<int:train_id>/seats/', methods=['GET'])
def get_seats_list_by_train_id(train_id):
    contents = request.json

    if user.is_admin(contents.get('user_id')):
        return jsonify(), Error.PERMISSION_DENIED

    return jsonify(seats=get_seats_by_train_id(train_id))


app.register_blueprint(module)
