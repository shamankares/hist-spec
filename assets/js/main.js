import * as events from './events.js';

document.addEventListener('DOMContentLoaded', events.loadAdditionalConfig);

const input = document.getElementById('inputImage');
const desired = document.getElementById('desiredHist');
const inputPreview = document.getElementById('previewInput');
const desiredPreview = document.getElementById('previewDesired');
input.addEventListener('change', () => events.updateImageDisplay(input, inputPreview));
desired.addEventListener('change', () => events.updateImageDisplay(desired, desiredPreview));

const form = document.getElementById('uploadImage');
form.addEventListener('submit', events.processImages);
