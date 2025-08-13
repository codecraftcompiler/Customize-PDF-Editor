// static/script.js

function selectTool(toolName) {
  const select = document.querySelector('select[name="operation"]');
  select.value = toolName;
}

const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const fileSelector = document.getElementById('fileSelector');

// Store file URLs and names
const fileMap = new Map();

fileInput.addEventListener('change', function () {
  // Clear previous state
  fileSelector.innerHTML = '<option disabled selected>Select a PDF to preview</option>';
  previewContainer.innerHTML = '';
  fileMap.clear();

  // Loop through uploaded files
  Array.from(this.files).forEach((file, index) => {
    if (file.type === "application/pdf") {
      const fileURL = URL.createObjectURL(file);
      fileMap.set(file.name, fileURL);

      const option = document.createElement('option');
      option.value = file.name;
      option.textContent = file.name;
      fileSelector.appendChild(option);
    }
  });
});

fileSelector.addEventListener('change', function () {
  previewContainer.innerHTML = ''; // Clear previous preview

  const selectedFileName = this.value;
  const fileURL = fileMap.get(selectedFileName);

  if (fileURL) {
    const iframe = document.createElement('iframe');
    iframe.src = fileURL;
    iframe.width = "100%";
    iframe.height = "500px";
    iframe.style.border = "1px solid gray";

    previewContainer.appendChild(iframe);
  }
});


function updatePreviewSelector() {
  fileSelector.innerHTML = '<option disabled selected>Select a PDF to preview</option>';
  fileMap.clear();
  previewContainer.innerHTML = '';

  fileBuffer.forEach(file => {
    if (file.type === "application/pdf") {
      const fileURL = URL.createObjectURL(file);
      fileMap.set(file.name, fileURL);

      const option = document.createElement('option');
      option.value = file.name;
      option.textContent = file.name;
      fileSelector.appendChild(option);
    }
  });
}



//  const fileInput = document.getElementById("fileInput");
  const fileHidden = document.getElementById("fileHidden");
  const fileListDisplay = document.getElementById("selectedFilesList");

  let fileBuffer = [];

  fileInput.addEventListener('change', () => {
  fileBuffer = Array.from(fileInput.files);
  updateFileList();
});

 function updateFileList() {
  fileListDisplay.innerHTML = "";
  fileBuffer.forEach((file, index) => {
    const li = document.createElement("li");
    li.textContent = file.name;

    const btn = document.createElement("button");
    btn.textContent = "Remove";
    btn.style.marginLeft = "1px";
    btn.onclick = () => {
      fileBuffer.splice(index, 1);  // Remove from buffer
      updateFileList();             // Refresh list + preview
    };

    li.appendChild(btn);
    fileListDisplay.appendChild(li);
  });

  // 🔁 Rebuild the real hidden input for submission
  const dataTransfer = new DataTransfer();
  fileBuffer.forEach(f => dataTransfer.items.add(f));
  fileHidden.files = dataTransfer.files;

  // 🔁 Refresh preview dropdown and iframe
  updatePreviewSelector();
}