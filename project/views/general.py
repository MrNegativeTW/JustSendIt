from flask import Blueprint, render_template, session, redirect, url_for, \
    request, flash, g, jsonify, abort, send_file
from project.model.formModel import UploadForm, ReceiveForm
from google.cloud import datastore
from google.cloud import storage
import hashlib
import tempfile

mod = Blueprint('general', __name__)

@mod.route('/', methods=['GET', 'POST'])
def index():
    global receiveForm
    receiveForm = ReceiveForm()

    if request.method == 'GET':
        return render_template('index.html', receiveForm=receiveForm, post=False)

    elif request.method == 'POST':
        # POST from receive form
        if receiveForm.submit.data:
            if receiveForm.validate_on_submit():
                fileId = receiveForm.fileID.data
                return redirect(url_for('receive.receiveFileID', fileID=fileId))
            return render_template('index.html', receiveForm=receiveForm, post=False)

        # Get uploaded file.
        uploaded_file = request.files.get('file')
        if not uploaded_file:
            return redirect(url_for('index'))

        # Generate md5 for file
        fileMD5 = hashlib.md5(uploaded_file.read()).hexdigest()
        uploaded_file.seek(0)

        # Get first 6 digis from md5 as fileCode
        fileCode = fileMD5[0:6]

        # Write file to cloud storage and make it public.
        client = storage.Client()
        bucket = client.get_bucket("justsendit")
        blob = bucket.blob(fileMD5)
        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )
        blob.make_public()

        # Write file detail to cloud datastore.
        if isFileDuplicate(fileMD5) == False:
            client = datastore.Client()
            task_key = client.key('fileDetails')
            entity = datastore.Entity(key=task_key)
            entity['fileCode'] = fileCode
            entity['fileFullMD5'] = fileMD5
            entity['filePublicUrl'] = blob.public_url
            entity['fileName'] = uploaded_file.filename
            client.put(entity)

        # The public URL can be used to directly access the uploaded file via HTTP.
        return render_template(
            'index.html',
            receiveForm=receiveForm,
            post=True,
            fileCode=fileCode)


'''Check duplicate file exists or not'''
def isFileDuplicate(fileFullMD5):
    client = datastore.Client()
    query = client.query(kind='fileDetails')
    query = query.add_filter('fileFullMD5', '=', fileFullMD5)
    result = query.fetch()
    resultLists = list(result)
    if len(resultLists) == 0:
        return False
    else:
        return True
