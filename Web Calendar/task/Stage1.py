from flask import Flask
from flask_restful import Api, Resource
import sys

app = Flask(__name__)
api = Api(app)


class HelloWorldResource(Resource):
    def get(self):
        return {"message": "Hello from the REST API!"}


class Event4Today(Resource):
    def get(self):
        return {"data": "There are no events for today!"}


api.add_resource(HelloWorldResource, '/hello')
api.add_resource(Event4Today, '/event/today')

# http://127.0.0.1:5000/hello

# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         arg_host, arg_port = sys.argv[1].split(':')
#         app.run(host=arg_host, port=arg_port)
#     else:
#         app.run()
