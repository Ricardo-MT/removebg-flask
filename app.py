import os
import io
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from flask import render_template
from rembg import remove
from PIL import Image

app = Flask(__name__)

load_dotenv()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.post("/remove_background/")
def remove_background():
    api_key = os.getenv('API_KEY')
    x_api_key = request.headers.get('x-api-key')
    if x_api_key != api_key:
        return jsonify({"message": "Not found"}), 404

    try:
        input_file = request.files['image']
        input_image = Image.open(io.BytesIO(input_file.read()))
    except Exception as e:
        return jsonify({"message": "Failed to read input image"}), 400
        
    try:
        output_image = remove(input_image)
    except Exception as e:
        return jsonify({"message": "Failed to process input image"}), 500
    
    output_file = io.BytesIO()
    try:
        output_image.save(output_file, format='PNG')
    except Exception as e:
        return jsonify({"message": "Failed to save output image"}), 500

    response = Response(response=output_file.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=output.png'
    response.headers['Content-Type'] = 'image/png'

    return response
