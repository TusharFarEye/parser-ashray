from flask import Flask
from waitress import serve
from routes import HealthCheck, Address
from service.Connections import conn

app = Flask(__name__)

def main():
    print(app)
    healthcheck = HealthCheck.HealthCheck()
    address = Address.Address()
    # @app.route('/', methods=['GET'])
    # def healthy():
    #     return ("healthy", 201, None)
    app.register_blueprint(healthcheck.health_app)
    app.register_blueprint(address.address_app)
    serve(app, host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
    conn.close()
