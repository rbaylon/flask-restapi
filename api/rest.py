from flask_restful import Api
from api.resources import Room, RoomList, ApiLogin
from baseapp import app

rest_api = Api(app)

# Build api routes
rest_api.add_resource(RoomList, '/api/rooms')
rest_api.add_resource(Room, '/api/rooms/<room_id>')
rest_api.add_resource(ApiLogin, '/api/login')
