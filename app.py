from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import os
import random

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/upload', methods=["POST"])
def index():
    S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
    S3_FILES_BUCKET_NAME = os.environ.get('BUCKET_NAME')
    LOCATION = os.environ.get('LOCATION')
    PASSWORD = os.environ.get('PASSWORD')

    if request.headers.get('password') != PASSWORD:
        return jsonify({'status':'invalid password'})
        
    file = request.files['file']
    
    if file is None:
        return jsonify({'status':'NO-OK'})

    s3 = boto3.client(
            service_name="s3",
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )

    filename = "{}_{}".format(random.getrandbits(128),file.filename)

    s3.upload_fileobj(file, S3_FILES_BUCKET_NAME, filename)
    
    url = f"https://{S3_FILES_BUCKET_NAME}.s3.{LOCATION}.amazonaws.com/{filename}"

    return jsonify({'status':'OK', 'url': url})

if __name__ == '__main__':
    app.debug = True
    app.run()