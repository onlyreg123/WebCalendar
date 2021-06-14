import datetime
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import sys

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Events.db'
parser = reqparse.RequestParser()

class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')


resource_fields = {
    'id':      fields.Integer,
    'event':   fields.String,
    'date':    MyDateFormat
}


class Event(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def save(self):
        # saves data into the table
        db.session.add(self)
        # commits changes
        db.session.commit()


db.create_all()

# deletes the row from the table.
# db.session.delete(event)


class HelloWorldResource(Resource):
    def get(self):
        return {"message": "Hello from the REST API!"}


class REvent4Today(Resource):
    # returns all rows from the table where the date column has today's date as a list of Car objects.
    # Event.query.filter(Event.date == datetime.date.today()).all()
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == datetime.date.today()).all()


class REvent(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # returns all rows from the table as a list of Event objects.
        return Event.query.all()
        # return {
        #     "message": "The event has been added!",
        #     "event": f"{args['event']}",
        #     "date": f"{args['date'].date()}"
        # }

    def post(self):
        args = parser.parse_args()
        my_event = Event(event=args['event'], date=args['date'].date())
        my_event.save()
        return {
            "message": "The event has been added!",
            "event": f"{args['event']}",
            "date": f"{args['date'].date()}"
        }


parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)

api.add_resource(HelloWorldResource, '/hello')
api.add_resource(REvent4Today, '/event/today')
api.add_resource(REvent, '/event')

# http://127.0.0.1:5000/hello
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run()
