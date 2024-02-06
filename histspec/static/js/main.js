const input = document.getElementById('inputImage');
const desired = document.getElementById('desiredHist');

const inputPreview = document.getElementById('preview');
const desiredPreview = document.getElementById('previewDesired');

const form = document.getElementById('uploadImage');

function updateImageDisplay(uploader, preview){
    while (preview.firstChild) {
        preview.removeChild(preview.firstChild);
    }

    const file = uploader.files[0];
    const image = document.createElement('img');
    image.src = URL.createObjectURL(file);
    preview.append(image);
}

async function processImages(event) {
    event.preventDefault();

    const resultPreview = document.getElementById('result');
    const placeholder = document.createElement('p');
    placeholder.textContent = 'Sedang diproses...';
    resultPreview.append(placeholder);

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

input.addEventListener('change', () => updateImageDisplay(input, inputPreview));
desired.addEventListener('change', () => updateImageDisplay(desired, desiredPreview));

form.addEventListener('submit', processImages);
