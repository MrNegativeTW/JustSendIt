from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file
from project.model.formModel import UploadForm, ReceiveForm
from google.cloud import datastore
from google.cloud import storage
import hashlib
import tempfile

mod = Blueprint('receive', __name__)


@mod.route('/receive/', methods=['GET', 'POST'])
def receive():
    return redirect(url_for('general.index'))


@mod.route('/receive/<fileID>', methods=['GET', 'POST'])
def receiveFileID(fileID):
    client = datastore.Client()
    query = client.query(kind='fileDetails')
    query = query.add_filter('fileCode', '=', fileID)
    result = query.fetch()
    resultLists = list(result)

    if len(resultLists) == 0:
        return 'No such file.', 400
    else:
        # client = storage.Client()
        # bucket = client.get_bucket("cloudcomputing-270803.appspot.com")
        # blob = bucket.blob(filename)
        # with tempfile.NamedTemporaryFile() as temp:
        #     blob.download_to_filename(temp.name)
        #     return send_file(temp.name, attachment_filename=filename)

        global filePublicUrls
        for key, value in resultLists[0].items():
            if key == 'filePublicUrl':
                filePublicUrls = value
        return render_template('receive.html', post=True, filePublicUrl=filePublicUrls)
