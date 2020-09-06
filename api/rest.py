from flask_restful import Api
from api.resources import Room, RoomList
from baseapp import app

rest_api = Api(app)

# Build api routes
rest_api.add_resource(RoomList, '/rooms')
rest_api.add_resource(Room, '/rooms/<room_id>')
