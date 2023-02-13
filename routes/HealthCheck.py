# from __main__ import app
from flask import Blueprint, render_template, abort

class HealthCheck:
    health_app = Blueprint('health_app', __name__, template_folder='templates')
    def __init__(self):
        # self.app = app
        pass

    @health_app.route('/healthz', methods=['GET'])
    def healthy():
        return ("healthy",201,None)

def hi():
    pass