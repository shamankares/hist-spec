from . import image

from flask import Flask, render_template, request, make_response

import os

def create_app(config=None):
  app = Flask(__name__, instance_relative_config=True)

  if config is None:
    if not app.config.from_pyfile('config.py', silent=True):
      app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
      app.config['MAX_CONTENT_LENGTH'] = os.getenv('MAX_CONTENT_LENGTH')
  else:
    app.config.from_mapping(config)
  
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

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

  return app

