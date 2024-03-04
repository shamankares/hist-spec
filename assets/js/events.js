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
  resultPreview.replaceChildren();

  const placeholder = document.createElement('p');
  placeholder.textContent = 'Processing...';
  resultPreview.append(placeholder);

  const form = document.getElementById('uploadImage');
  const url = form.getAttribute('action');
  const formData = new FormData(form);

  await fetch(url, {
    method: 'POST',
    body: formData,
  })
  .then((res) => {
    if (res.ok) return res.blob();

    return res.json().then(({
      message: errorMessage,
      statusCode,
    }) => {
      if (statusCode === 500) {
        throw new Error('Something is wrong in server. Try again later.');
      }
      throw new Error(errorMessage);
    });        
  })
  .then(renderResult)
  .catch(renderError);
}

function renderResult(blob) {
  const resultPreview = document.querySelector('#result .preview');
  resultPreview.replaceChildren();

  const objectUrl = URL.createObjectURL(blob)
  const img = document.createElement('img');
  img.src = objectUrl;

  const downloadWrapper = document.createElement('div');
  downloadWrapper.setAttribute('class', 'link-btn-wrapper');

  const downloadAttrib = document.createAttribute('download');
  const downloadLink = document.createElement('a');
  downloadLink.setAttribute('href', objectUrl);
  downloadLink.setAttribute('draggable', false);
  downloadLink.setAttributeNode(downloadAttrib);

  const downloadButton = document.createElement('button');
  downloadButton.textContent = 'Download Image';
  
  downloadLink.append(downloadButton);
  downloadWrapper.append(downloadLink);

  resultPreview.append(img, downloadWrapper);
}

function renderError(errorMessage) {
  const messageElement = document.querySelector('#result .preview p');
  messageElement.textContent = errorMessage;
}
