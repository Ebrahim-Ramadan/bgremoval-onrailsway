from flask import Flask, request, send_file, jsonify
import rembg
import numpy as np
from PIL import Image
import io
import os
app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({'message': 'Hello World!'})
@app.route('/', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        input_image = Image.open(file.stream)

        input_array = np.array(input_image)

        output_array = rembg.remove(input_array)
        output_image = Image.fromarray(output_array)

        output_image = output_image.convert('RGB')

        img_io = io.BytesIO()
        output_image.save(img_io, 'JPEG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='output_image.jpg')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
