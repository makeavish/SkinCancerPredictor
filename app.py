from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.inception_v3 import InceptionV3,preprocess_input,decode_predictions
from keras.models import load_model
from keras.preprocessing.image import img_to_array,load_img

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/finalModel.h5'

# Load your trained model

# loading the model
from keras.models import model_from_json
with open('models/model_to_json.json', 'r') as json_file:
    loaded_model_json = json_file.read()    
    model = model_from_json(loaded_model_json)
    model.load_weights(MODEL_PATH)
    print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')

def pred(img_path):    
    img = load_img(img_path,target_size = (299,299)) #Load the image and set the target size to the size of input of our model
    x = img_to_array(img) #Convert the image to array
    x = np.expand_dims(x,axis=0) #Convert the array to the form (1,x,y,z) 
    x = preprocess_input(x) # Use the preprocess input function o subtract the mean of all the images
    k = model.predict(x)
    print(k)
    p = np.argmax(k) # Store the argmax of the predictions
    if p==0:     # P=0 for basal,P=1 for melanoma , P=2 for squamous
        return "benign"
    else:
        return "malignant"

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', predicted='waiting to run')
    # return ""

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        file = request.files['file']
        if file.filename == '':
            raise InvalidUsage('No image selected for uploading',status_code=400)
        if file and allowed_file(file.filename):
            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, 'uploads', secure_filename(file.filename))
            file.save(file_path)

            # Make prediction
            preds = pred(file_path)
            return render_template('index.html', predicted=preds)
        else:
            raise InvalidUsage('Incorrect image format selected for uploading',status_code=400)
    return None


if __name__ == '__main__':
    app.run(debug=True)