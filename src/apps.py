from flask import Flask
from flask_restful import Api

from src.resources.service import ServiceResource
from src.resources.service_list import ServiceListResource

from src.resources.property import PropertyResource
from src.resources.property_list import PropertyListResource

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(app)

api.add_resource(ServiceResource, '/services/<string:service_id>')
api.add_resource(ServiceListResource, '/services')

api.add_resource(PropertyResource, '/services/<string:service_id>/properties/<string:property_id>')
api.add_resource(PropertyListResource, '/services/<string:service_id>/properties')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3010, debug=True)