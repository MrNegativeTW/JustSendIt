from flask import Flask, render_template, request, redirect, url_for, send_file, abort

# App Start
app = Flask(__name__)
app.config.from_object('websiteconfig')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', errorCode=404), 404

@app.errorhandler(500)
def inter_server_error(error):
    return render_template('error.html', errorCode=500), 500

from project.views import general
from project.views import receive
from project.views import manualError
app.register_blueprint(general.mod)
app.register_blueprint(receive.mod)
app.register_blueprint(manualError.mod)
