document.getElementById("cropForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const getInputValue = (id) => {
        const value = parseFloat(document.getElementById(id).value);
        return isNaN(value) ? null : value;
    };

    const data = {
        N: getInputValue("nitrogen"),
        P: getInputValue("phosphorus"),
        K: getInputValue("potassium"),
        temperature: getInputValue("temperature"),
        humidity: getInputValue("humidity"),
        ph: getInputValue("ph"),
        rainfall: getInputValue("rainfall"),
    };

    if (Object.values(data).includes(null)) {
        document.getElementById("result").innerText = "Please fill all fields correctly!";
        return;
    }

    document.getElementById("result").innerText = "Predicting crop...";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById("result").innerText = result.error ? `Error: ${result.error}` : `Recommended Crop: ${result.crop}`;
    } catch (error) {
        document.getElementById("result").innerText = "Error in prediction!";
    }
});
