from flask import Flask, render_template, request, make_response

from imgench import image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.post('/process')
def process_image():
    uploads = request.files
    files = {}

    for key, file in uploads.items():
        file_stream = file.stream.read()
        files[key] = image.create_image(file_stream)
    
    result = image.process_image(files['input_image'], files['desired_image'])
    
    response = make_response(result.getvalue())
    response.mimetype = 'image/png'

    return response
