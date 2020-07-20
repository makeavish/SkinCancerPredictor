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
from flask import Flask, redirect, url_for, request, render_template
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


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', predicted='waiting to run')
    # return ""


@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = pred(file_path)
        return render_template('index.html', predicted=preds)
    return None


if __name__ == '__main__':
    app.run(debug=True)