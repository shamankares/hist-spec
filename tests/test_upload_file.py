from pathlib import Path

resource = Path(__file__).parent / "resources"

def test_upload_invalid_property(client):
  response_no_input_image = client.post("/process", data={
    "desiredImage": (resource/"tepi_pantai.jpg").open("rb")
  })

  res_no_input_image_json = response_no_input_image.get_json()

  assert res_no_input_image_json['statusCode'] == 400
  assert res_no_input_image_json['status'] == 'failed'
  assert res_no_input_image_json['message'] == "Missing 'inputImage' property"

  response_no_desired_image = client.post("/process", data={
    "inputImage": (resource/"tepi_pantai.jpg").open("rb")
  })

  res_no_desired_image_json = response_no_desired_image.get_json()

  assert res_no_desired_image_json['statusCode'] == 400
  assert res_no_desired_image_json['status'] == 'failed'
  assert res_no_desired_image_json['message'] == "Missing 'desiredImage' property"

def test_upload_invalid_image_file(client):
  response_invalid_input_image = client.post("/process", data={
    "inputImage": (resource/"test.txt").open("rb"),
    "desiredImage": (resource/"tepi_pantai.jpg").open("rb")
  })

  res_invalid_input_image_json = response_invalid_input_image.get_json()

  assert res_invalid_input_image_json['statusCode'] == 400
  assert res_invalid_input_image_json['status'] == 'failed'
  assert res_invalid_input_image_json['message'] == 'inputImage must be an image file'

  response_invalid_desired_image = client.post("/process", data={
    "inputImage": (resource/"tepi_pantai.jpg").open("rb"),
    "desiredImage": (resource/"test.txt").open("rb")
  })

  res_invalid_desired_image_json = response_invalid_desired_image.get_json()

  assert res_invalid_desired_image_json['statusCode'] == 400
  assert res_invalid_desired_image_json['status'] == 'failed'
  assert res_invalid_desired_image_json['message'] == 'desiredImage must be an image file'

def test_upload_too_large_image_file(client):
  response_large_input_image = client.post("/process", data={
    "inputImage": (resource/"cumi_naik_mouse.png").open("rb"),
    "desiredImage": (resource/"tepi_pantai.jpg").open("rb")
  })

  res_large_input_image_json = response_large_input_image.get_json()

  assert res_large_input_image_json['statusCode'] == 413
  assert res_large_input_image_json['status'] == 'failed'
  assert res_large_input_image_json['message']

  response_large_desired_image = client.post("/process", data={
    "inputImage": (resource/"tepi_pantai.jpg").open("rb"),
    "desiredImage": (resource/"cumi_naik_mouse.png").open("rb")
  })

  res_large_desired_image_json = response_large_desired_image.get_json()

  assert res_large_desired_image_json['statusCode'] == 413
  assert res_large_desired_image_json['status'] == 'failed'
  assert res_large_desired_image_json['message']

def test_upload_image_file(client):
  response = client.post("/process", data={
    "inputImage": (resource/"tepi_pantai.jpg").open("rb"),
    "desiredImage": (resource/"cumi_naik_mouse_small.jpg").open("rb")
  })
  
  assert response.content_type == 'image/png'
