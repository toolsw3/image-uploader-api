from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import os
import random
import sys

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/upload', methods=["POST"])
def index():
    try:
        S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
        S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
        S3_FILES_BUCKET_NAME = os.environ.get('BUCKET_NAME')
        LOCATION = os.environ.get('LOCATION')
        PASSWORD = os.environ.get('PASSWORD')
        print(S3_ACCESS_KEY, file=sys.stderr)
        print(S3_SECRET_KEY, file=sys.stderr)
        print(S3_FILES_BUCKET_NAME, file=sys.stderr)
        print(LOCATION, file=sys.stderr)
        print(PASSWORD, file=sys.stderr)
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
    except Exception as error:
        print(str(error), file=sys.stderr)
        return jsonify({'status':'ERROR'})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
