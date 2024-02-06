from werkzeug.exceptions import BadRequest

required = ['inputImage', 'desiredImage']

def validate_request_properties(req):
  for prop in required:
    if prop not in req.files:
      raise BadRequest(description=f"Missing '{prop}' property")

def validate_images(req):
  for prop in required:
    file = req.files[prop]
    content_type = file.content_type

    if 'image' not in content_type:
      raise BadRequest(description=f"'{prop}' must be an image file")
