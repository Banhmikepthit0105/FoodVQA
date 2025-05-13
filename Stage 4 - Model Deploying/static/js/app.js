document.addEventListener('DOMContentLoaded', function() {
    // Lấy các phần tử DOM
    const uploadContainer = document.getElementById('uploadContainer');
    const imageUpload = document.getElementById('imageUpload');
    const previewImage = document.getElementById('previewImage');
    const uploadContent = document.getElementById('uploadContent');
    const imageInfo = document.getElementById('imageInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const askButton = document.getElementById('askButton');
    const questionInput = document.getElementById('questionInput');
    const initialState = document.getElementById('initialState');
    const loadingState = document.getElementById('loadingState');
    const answerContent = document.getElementById('answerContent');
    const answerText = document.getElementById('answerText');
    const modelUsed = document.querySelector('#modelUsed span');

    if (!uploadContainer || !imageUpload || !previewImage || !uploadContent || !imageInfo || !askButton || !questionInput || !answerContent || !answerText || !modelUsed) {
        console.error("One or more elements are missing.");
        return;
    }

    uploadContainer.addEventListener('click', function() {
        imageUpload.click(); // Mở cửa sổ chọn file
    });

    // Khi người dùng chọn file, hiển thị ảnh preview
    imageUpload.addEventListener('change', function(e) {
        if (e.target.files.length) {
            const file = e.target.files[0]; 
            const reader = new FileReader();
            
            reader.onload = function(event) {
                previewImage.src = event.target.result;  
                previewImage.classList.remove('hidden'); 
                uploadContent.classList.add('hidden'); 
                imageInfo.classList.remove('hidden');
                
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
            };
            
            reader.readAsDataURL(file); 
        }
    });
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Question handling
    askButton.addEventListener('click', function() {
        if (!previewImage.src || previewImage.classList.contains('hidden')) {
            alert('Please upload an image first');
            return;
        }
        
        const question = questionInput.value.trim();
        if (!question) {
            alert('Please enter a question');
            return;
        }
        
        const selectedModel = document.querySelector('input[name="model"]:checked').value;
        
        initialState.classList.add('hidden');
        loadingState.classList.remove('hidden');
        answerContent.classList.add('hidden');
        
        const formData = new FormData();
        formData.append('image', imageUpload.files[0]);  
        formData.append('question', question); 
        formData.append('model', selectedModel); 
        
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingState.classList.add('hidden');
            answerText.innerHTML = data.answer;
            modelUsed.textContent = data.model;
            // Không hiển thị Confidence nữa
            answerContent.classList.remove('hidden');
        })
        .catch(error => {
            loadingState.classList.add('hidden');
            alert('Error: ' + error.message);
        });
    });
});
