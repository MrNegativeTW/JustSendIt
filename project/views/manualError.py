from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file

mod = Blueprint('manualError', __name__)


@mod.route('/404', methods=['GET'])
def manual_not_found():
    return render_template('error.html', errorCode=404)

@mod.route('/500', methods=['GET'])
def manual_inter_server_error():
    return render_template('error.html', errorCode=500)