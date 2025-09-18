from flask import Flask
from src.controller.authenticate_controller import authenticate_controller
from src.controller.company_controller import company_controller
from src.controller.report_controller import report_controller

app = Flask(__name__)
app.register_blueprint(authenticate_controller, url_prefix="/v1")
app.register_blueprint(company_controller, url_prefix="/v1/company")
app.register_blueprint(report_controller, url_prefix="/v1/report")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
