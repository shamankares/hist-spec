from . import image, validator

from flask import Flask, request, make_response
from werkzeug.exceptions import HTTPException

import os
import json

def create_app(config=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000

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

  @app.errorhandler(HTTPException)
  def handle_exception(err):
    response = err.get_response()
    response.data = json.dumps({
        "statusCode": err.code,
        "status": 'failed',
        "message": err.description,
    })
    response.content_type = "application/json"
    return response

  @app.post('/process')
  def process_image():
    try:
      validator.validate_request_properties(request)
      validator.validate_images(request)
    except HTTPException as err:
      raise err

    uploads = request.files
    files = {}

    for key, file in uploads.items():
        file_stream = file.stream.read()
        files[key] = image.create_image(file_stream)
    
    result = image.process_image(files['inputImage'], files['desiredImage'])
    
    response = make_response(result.getvalue())
    response.mimetype = 'image/png'

    return response

  return app

