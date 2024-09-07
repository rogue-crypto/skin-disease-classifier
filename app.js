document.getElementById('uploadBtn').addEventListener('click', function() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please upload an image");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // Replace the URL with your backend URL after deploying on Render
    fetch('https://your-flask-app.onrender.com/predict', {  // Replace with actual Render URL
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `Predicted Disease: ${data.predicted_class} <br> Confidence: ${data.confidence.toFixed(2)}`;
        if (data.gemini_info && !data.gemini_info.error) {
            resultDiv.innerHTML += `<br> Gemini API Data: ${JSON.stringify(data.gemini_info)}`;
        } else {
            resultDiv.innerHTML += `<br> Error from Gemini API: ${data.gemini_info.error}`;
        }
    })
    .catch(error => console.error('Error:', error));
});
