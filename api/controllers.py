from baseapp.models import Rooms
from baseapp import db

class RoomsController:
    def add(self, room):
        existing = Rooms.query.filter_by(roomid=room['roomid']).first()
        if not existing:
            new_room = Rooms()
            new_room.yourname = room['yourname']
            new_room.meetingpwd = room['meetingpwd']
            new_room.roomname = room['roomname']
            new_room.tmp = room['tmp']
            new_room.roomid = room['roomid']

            db.session.add(new_room)
            db.session.commit()
            return True

        return False

    def edit(self, room):
        existing_room = Rooms.query.filter_by(roomid=room['roomid']).first()
        if existing_room:
            existing_room.meetingpwd = room['meetingpwd']
            db.session.commit
            return True

        return False


    def delete(self, room):
        existing_room = Rooms.query.filter_by(roomid=room['roomid']).first()
        if existing_room:
            db.session.delete(existing_room)
            db.session.commit()
            return True

        return False
