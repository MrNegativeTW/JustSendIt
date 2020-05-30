from flask import Flask, render_template, request, redirect, send_file, abort
from loginModel import UploadForm
from google.cloud import datastore
from google.cloud import storage
# from google.cloud.storage import Blob
import hashlib
import tempfile

# Cloud Storage Client Libraries
# https://cloud.google.com/storage/docs/reference/libraries#client-libraries-usage-python

# App Start
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a83c51c8b7fc804eb395d7c1d753fa28'


# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if request.method == 'GET':
        return render_template('index.html', form=form, post=False)
    elif request.method == 'POST':

        # https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage?hl=zh-tw
        uploaded_file = request.files.get('file')
        if not uploaded_file:
            return 'No file uploaded, fool.', 400

        # Generate md5 for file
        fileMD5 = hashlib.md5(uploaded_file.read()).hexdigest()
        uploaded_file.seek(0)

        # Write file to cloud storage and make it public.
        client = storage.Client()
        bucket = client.get_bucket("cloudcomputing-270803.appspot.com")
        blob = bucket.blob(uploaded_file.filename)
        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )
        blob.make_public()

        # Get file's public url and MD5
        filePublicUrl = blob.public_url
        fileCode = fileMD5[0:6]
        # fileName = request.files['file'].name
        print(filePublicUrl)
        print(fileCode)
        # print(fileName)
    
        # Write file's public url and MD5 to cloud datastore.
        # @link https://googleapis.dev/python/datastore/latest/client.html
        client = datastore.Client()
        task_key = client.key('fileDetails')
        entity = datastore.Entity(key=task_key)
        entity['fileCode'] = fileCode
        entity['filePublicUrl'] = filePublicUrl
        # entity['fileName'] = fileName
        client.put(entity)

        # The public URL can be used to directly access the uploaded file via HTTP.
        return render_template('index.html', form=form, post=True, fileCode=fileCode)


@app.route('/receive/<fileID>', methods=['GET', 'POST'])
def receive(fileID):
    form = UploadForm()

    client = datastore.Client()
    query = client.query(kind='fileDetails')
    query = query.add_filter('fileCode', '=', fileID)
    result = query.fetch()
    resultLists = list(result)

    if len(resultLists) == 0:
        # return render_template('index.html', form=form, post=False)
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
        return render_template('receive.html', form=form, post=True, filePublicUrl=filePublicUrls)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(debug=True)