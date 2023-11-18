# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from moviepy.editor import VideoFileClip
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import ffmpeg
from scipy.spatial import distance


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/get_similar', methods=['POST'])
def cosine_similarity():
    data = request.json
    query_vector = data['query_vector']
    vector_text_pairs = data['vectors']

    # Extract embeddings and their corresponding texts
    vectors = [pair['embeddings'] for pair in vector_text_pairs]
    texts = [pair['text'] for pair in vector_text_pairs]

    # Calculate cosine similarity for each vector
    # Return the index of the most similar vector
    most_similar_index = max(range(len(vectors)), key=lambda index: 1 - distance.cosine(query_vector, vectors[index]))

    return jsonify({'most_similar_text': texts[most_similar_index]})

@app.route('/get_video_duration', methods=['POST'])
def get_video_duration():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return "URL do vídeo é necessária", 400

    try:
        # Baixando o vídeo para a memória
        video_data = requests.get(video_url).content
        video_file = BytesIO(video_data)

        # Usando moviepy para ler a duração
        with VideoFileClip(video_file) as clip:
            duration = clip.duration

        return jsonify({"duration": duration})
    except Exception as e:
        return f"Erro ao processar a solicitação: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)

