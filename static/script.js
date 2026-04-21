document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = 'Processing...';
    resultDiv.style.backgroundColor = '#eee';

    // Build the data object exactly as your FastAPI Pydantic model expects
    const payload = {
        Name: document.getElementById('Name').value,
        Age: parseFloat(document.getElementById('Age').value),
        Gender: document.getElementById('Gender').value,
        Blood_Type: document.getElementById('Blood_Type').value,
        Medical_Condition: document.getElementById('Medical_Condition').value,
        Doctor: document.getElementById('Doctor').value,
        Hospital: document.getElementById('Hospital').value,
        Insurance_Provider: document.getElementById('Insurance_Provider').value,
        Billing_Amount: parseFloat(document.getElementById('Billing_Amount').value),
        Room_Number: parseInt(document.getElementById('Room_Number').value),
        Admission_Type: document.getElementById('Admission_Type').value,
        Medication: document.getElementById('Medication').value,
        Days_in_hospital: parseInt(document.getElementById('Days_in_hospital').value)
    };

    try {
        const response = await fetch('./predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.prediction) {
            resultDiv.innerHTML = `Prediction: ${data.prediction[0]}`;
            resultDiv.style.backgroundColor = data.prediction[0] === 'Normal' ? '#d4edda' : '#f8d7da';
            resultDiv.style.color = data.prediction[0] === 'Normal' ? '#155724' : '#721c24';
        } else {
            resultDiv.innerHTML = `Error: ${data.error}`;
        }
    } catch (error) {
        resultDiv.innerHTML = 'Error connecting to the server.';
        console.error(error);
    }
});
