from flask_restx import Namespace, Resource

ping_namespace = Namespace("ping")

class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "You have pinged the hair-talk backend service!"}
    
ping_namespace.add_resource(Ping, "")   