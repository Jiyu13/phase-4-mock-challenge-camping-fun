from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
# 1. import flask_restful
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# 2. connect flask_restful to app
api = Api(app)

# 3.remove the routes index route
# @app.route('/')
# def index():
#     response = make_response(
#         {
#             "message": "Hello Campers!"
#         },
#         200
#     )
#     return response

class Campers(Resource):
    def get(self):
        campers = Camper.query.all()
        campers_dict = [camper.to_dict() for camper in campers]
        return make_response(jsonify(campers_dict), 200)

    
    def post(self):
        try:
            new_camper = Camper(
                name=request.get_json()['name'],
                age=request.get_json()['age']
            )
            db.session.add(new_camper)
            db.session.commit()
            response = make_response(new_camper.to_dict(), 201)

        except Exception as e:
            # If the Camper is not created successfully, return the following JSON data, along with the appropriate HTTP status code:
            message = {
                "errors": "invalid input"
            }
            response = make_response(message, 422)
        return response
api.add_resource(Campers, '/campers')


class CamperByID(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            message = {
                "error": "Camper not found"
            }
            return make_response(message, 404)
        return make_response(camper.to_dict(), 200)
api.add_resource(CamperByID, '/campers/<int:id>')


class Activities(Resource):
    def get(self):
        activities = Activity.query.all()
        activities_dict_list = [activity.to_dict() for activity in activities]
        return make_response(activities_dict_list, 200)
api.add_resource(Activities, '/activities')


class ActivityByID(Resource):
    # activity = Activity.query.filter(id == id).first()  #
    def get(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            response_body = {
                "error": "Activity not found"
            }
            return make_response(response_body.to_dict(), 404)
        return make_response(activity.to_dict(), 200)

    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            # If the Activity does not exist, return the following JSON data, along with the appropriate HTTP status code:
            message = {
                "error": "Activity not found"
            }
            return make_response(message, 404)
        
        db.session.delete(activity)
        db.session.commit()
        return make_response({}.to_dict(), 200)

api.add_resource(ActivityByID, '/activities/<int:id>')


class Signups(Resource):
    def get(self):
        signups = Signup.query.all()
        signups_dict = [signup.to_dict() for signup in signups]
        return make_response(signups_dict, 200)

    def post(self):
        new_signup = Signup(
            time=request.get_json()['time'],
            camper_id=request.get_json()['camper_id'],
            activity_id=request.get_json['activity_id']
        )
        # If the Signup is created successfully, send back a response with the data related to the Activity:
        return make_response(new_signup.activity.to_dict(), 201)
        
        # If the Signup is not created successfully, return the following JSON data, along with the appropriate HTTP status code:
api.add_resource(Signups, '/signups')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
