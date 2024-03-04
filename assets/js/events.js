export function loadAdditionalConfig() {
  const form = document.getElementById('uploadImage');
  form.setAttribute(
    'action',
    `${process.env.BACKEND_PROTOCOL}://${process.env.BACKEND_DOMAIN}:${process.env.BACKEND_PORT}/process`
  );
}

export function updateImageDisplay(uploader, preview){
  while (preview.firstChild) {
      preview.removeChild(preview.firstChild);
  }

  const file = uploader.files[0];
  const image = document.createElement('img');
  image.src = URL.createObjectURL(file);
  preview.append(image);
}

export async function processImages(event) {
  event.preventDefault();

  const resultPreview = document.querySelector('#result .preview');
  const placeholder = document.createElement('p');
  placeholder.textContent = 'Processing...';
  resultPreview.append(placeholder);

  const form = document.getElementById('uploadImage');
  const url = form.getAttribute('action');
  const formData = new FormData(form);
  const result = await fetch(url, {
      method: 'POST',
      body: formData,
  })
  .then((res) => res.blob())
  .then((blob) => URL.createObjectURL(blob));
  
  while (resultPreview.firstChild) {
      resultPreview.removeChild(resultPreview.firstChild);
  }

  const img = document.createElement('img');
  img.src = result;
  resultPreview.append(img);
}
