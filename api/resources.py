from flask import request, jsonify
from flask_restful import reqparse, abort, Resource
from werkzeug.security import check_password_hash
from jwttoken import jwt, jwt_required, create_access_token
from uuid import uuid4


ROOMS = {
    '123456789000000000000000000000000000': {
        'your_name': 'Test01',
        'meeting_pwd': 'password123',
        'room_name': 'Room01'
    },
    'abc456789000000000000000000000000000': {
        'your_name': 'Test02',
        'meeting_pwd': 'password123',
        'room_name': 'Room02',
    }
}


def abort_if_room_doesnt_exist(room_id):
    if room_id not in ROOMS:
        abort(404, message="Room {} doesn't exist".format(room_id))

parser = reqparse.RequestParser()
parser.add_argument('your_name', required=True)
parser.add_argument('meeting_pwd', required=True)
parser.add_argument('room_name', required=True)

# Authentication
class ApiLogin(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        user = Users.query.filter_by(username=auth.username).first()

        if check_password_hash(user.password, auth.password) and user:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

        return jsonify({"msg": "Invalid username or password"}), 401

# Single resource
class Room(Resource):
    @jwt_required
    def get(self, room_id):
        abort_if_room_doesnt_exist(room_id)
        return ROOMS[room_id]

    @jwt_required
    def delete(self, room_id):
        abort_if_room_doesnt_exist(room_id)
        del ROOMS[room_id]
        return '', 204

    @jwt_required
    def put(self, room_id):
        request.get_json(force=True)
        args = parser.parse_args()
        room = {
            'your_name': args['your_name'],
            'meeting_pwd': args['meeting_pwd'],
            'room_name': args['room_name']
        }
        ROOMS[room_id] = room
        return room, 201


# Multiple resource + add resource
class RoomList(Resource):
    @jwt_required
    def get(self):
        return ROOMS

    @jwt_required
    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        room_id = str(uuid4())
        ROOMS[room_id] = {
            'your_name': args['your_name'],
            'meeting_pwd': args['meeting_pwd'],
            'room_name': args['room_name']
        }
        return ROOMS[room_id], 201
