// Tab switching logic
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const aaboutus = document.querySelector("#aabout-us");
const aboutus = document.querySelector("#about-us");
const home = document.querySelector("#home");
const footer = document.querySelector("footer")
const anchors = document.q

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active from all tabs
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        // Add active to selected tab
        button.classList.add('active');
        const selectedTab = document.getElementById(button.dataset.tab);
        selectedTab.classList.add('active');
    });
});

// Image Analysis Logic
const analyzeButtons = document.querySelectorAll('.analyze-btn');

analyzeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const parentTab = button.closest('.tab-content');
        const fileInput = parentTab.querySelector('input[type="file"]');
        const resultBox = parentTab.querySelector('.result');
        resultBox.classList.add("active");

        if (fileInput.files.length === 0) {
            alert("Please upload an image before analyzing.");
            return;
        }

        const file = fileInput.files[0];
        const condition = parentTab.id; // e.g., "brain-tumor"
        const formData = new FormData();
        formData.append("image", file);

        // Show loading message
        resultBox.innerHTML = `<p style="color: blue;">Analyzing...</p>`;

        // Call Flask backend
        fetch(`http://localhost:5000/predict/${condition}`, {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            resultBox.innerHTML = `
                <h4>Result: <span>${data.result}</span></h4>
                <p>Confidence: ${data.confidence}</p>
            `;
        })
        .catch(err => {
            resultBox.innerHTML = "<p style='color:red;'>Prediction failed.</p>";
            console.error(err);
        });
    });
});