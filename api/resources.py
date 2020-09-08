from flask import request, jsonify, make_response
from flask_restful import reqparse, abort, Resource
from werkzeug.security import check_password_hash
from uuid import uuid4
from baseapp.models import Users
from baseapp import app
from api.controllers import RoomsController
from baseapp.models import Rooms
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

jwt = JWTManager(app)


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


def abort_if_room_doesnt_exist(roomid):
    room = Rooms.query.filter_by(roomid = roomid).first()
    if not room:
        abort(404, message="Room ID {} doesn't exist".format(roomid))

    return room

parser = reqparse.RequestParser()
parser.add_argument('yourname', required=True)
parser.add_argument('meetingpwd', required=True)
parser.add_argument('roomname', required=True)

# Authentication
class ApiLogin(Resource):
    def post(self):
        if not request.is_json:
            return make_response('Could not verify', 400, {"msg": "Missing JSON in request"})

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return make_response('Could not verify', 400, {"msg": "Missing username parameter"})
        if not password:
            return make_response('Could not verify', 400, {"msg": "Missing password parameter"})

        user = Users.query.filter_by(username=username).first()

        if check_password_hash(user.password, password) and user:
            access_token = str(create_access_token(identity=username))
            return make_response({"access_token": access_token}, 200, {"msg": 'success'})

        return make_response('Could not verify', 401, {"msg": "Invalid username or password"})

# Single resource
class Room(Resource):
    @jwt_required
    def get(self, room_id):
        room = abort_if_room_doesnt_exist(room_id)
        r = {
            'yourname': room.yourname,
            'meetingpwd': room.meetingpwd,
            'roomname': room.roomname,
            'roomid': room.roomid
        }
        return r

    @jwt_required
    def delete(self, room_id):
        rc = RoomsController()
        abort_if_room_doesnt_exist(room_id)
        r = {}
        r['roomid'] = room_id

        if rc.delete(r):
            return r, 204

        return {'msg': 'Failed to delete record!'}, 404

    @jwt_required
    def put(self, room_id):
        request.get_json(force=True)
        rc = RoomsController()
        args = parser.parse_args()
        r = {}
        r['yourname'] = args['yourname']
        r['meetingpwd'] = args['meetingpwd']
        r['roomname'] = args['roomname']
        r['roomid'] = room_id

         # do validation before calling rc.edit
        if rc.edit(r):
            return r, 201

        return {'msg': 'Failed to update record!'}, 404


# Multiple resource + add resource
class RoomList(Resource):
    @jwt_required
    def get(self):
        rooms = Rooms.query.all()
        roomlist = { "rooms": [] }
        for room in rooms:
            r = {}
            r['Room Name'] = room.roomname
            r['Creator'] = room.yourname
            r['Room ID'] = room.roomid
            roomlist['rooms'].append(r)
        return roomlist

    @jwt_required
    def post(self):
        request.get_json(force=True)
        rc = RoomsController()
        args = parser.parse_args()
        room_id = str(uuid4())
        r = {}
        r['yourname'] = args['yourname']
        r['meetingpwd'] = args['meetingpwd']
        r['roomname'] = args['roomname']
        r['roomid'] = room_id
        r['tmp'] = True

        # do validation before calling rc.add
        if rc.add(r):
            return r, 201

        return {'msg': 'Failed to add record!'}, 400
