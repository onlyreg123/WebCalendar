from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs
from datetime import datetime

import sys

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class HelloWorldResource(Resource):
    def get(self):
        return {"message": "Hello from the REST API!"}


class Event4Today(Resource):
    def get(self):
        return {"data": "There are no events for today!"}


class Event(Resource):
    def post(self):
        args = parser.parse_args()
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
api.add_resource(Event4Today, '/event/today')
api.add_resource(Event, '/event')

# http://127.0.0.1:5000/hello

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run()
