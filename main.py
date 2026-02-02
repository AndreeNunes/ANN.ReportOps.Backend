from flask import Flask
from flask_cors import CORS

from src.controller.ordem_service_attachment_controller import ordem_service_attachment_controller
from src.controller.equipament_controller import equipament_controller
from src.controller.authenticate_controller import authenticate_controller
from src.controller.company_controller import company_controller
from src.controller.report_controller import report_controller
from src.controller.client_controller import client_controller

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(authenticate_controller, url_prefix="/v1")
app.register_blueprint(company_controller, url_prefix="/v1/company")
app.register_blueprint(report_controller, url_prefix="/v1/report")
app.register_blueprint(equipament_controller, url_prefix="/v1/equipament")
app.register_blueprint(ordem_service_attachment_controller, url_prefix="/v1/ordem-service-attachment")
app.register_blueprint(client_controller, url_prefix="/v1/client")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
