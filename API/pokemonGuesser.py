from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import PIL.Image as Image
import numpy as np


app = Flask(__name__)


@app.route('/pokemon/type/guess', methods=['POST'])
def predict_type():
    # Check if the POST request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file in request'}), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'File is empty'}), 400

    prediction = model_type_predict(file, 256)

    return jsonify({'prediction': prediction})


@app.route('/pokemon/guess', methods=['POST'])
def predict_pokemon():
    # Check if the POST request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file in request'}), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'File is empty'}), 400

    prediction = model_pokemon_predict(file, 256)

    return jsonify({'prediction': prediction})


def model_pokemon_predict(file, size):
    img = Image.open(file)
    img = img.convert('RGB')
    img = img.resize((size, size))

    image_array = img_to_array(img) / 255.0

    # Reshape the image array to match the input shape of the model
    image_array = np.expand_dims(image_array, axis=0)

    model = keras.models.load_model('../guess_pokemon.h5')

    # Predict using the model
    predictions = model.predict(image_array)

    # Load the labels
    pokemon_labels = np.load('../pokemons_labels.npy')
    predicted_label = pokemon_labels[np.argmax(predictions)]

    return predicted_label


def model_type_predict(file, size):
    img = Image.open(file)
    img = img.convert('RGB')
    img = img.resize((size, size))

    image_array = img_to_array(img) / 255.0

    # Reshape the image array to match the input shape of the model
    image_array = np.expand_dims(image_array, axis=0)

    model = keras.models.load_model('../guess_type.h5')

    # Predict using the model
    predictions = model.predict(image_array)

    # Load the labels
    unique_labels = np.load('../unique_labels.npy')
    predicted_label = unique_labels[np.argmax(predictions)]

    return predicted_label


CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


if __name__ == '__main__':
    app.run()