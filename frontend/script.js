async function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<div class='loading'>⏳ Processing... Please wait.</div>";

    try {

        fetch("https://creditcard-fraud-ml.onrender.com/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        if (!data.length) {
            resultDiv.innerHTML = "No data returned.";
            return;
        }

        displayTable(data);

    } catch (error) {
        resultDiv.innerHTML = `<div style="color:red;">Error: ${error.message}</div>`;
    }
}

function displayTable(data) {

    let fraudCount = 0;

    let tableHTML = "<div class='table-container'>";
    tableHTML += "<table class='result-table'><tr>";

    // Headers
    const keys = Object.keys(data[0]);
    keys.forEach(key => {
        tableHTML += `<th>${key}</th>`;
    });

    tableHTML += "</tr>";

    // Rows
    data.forEach(row => {

        if (row["Prediction"] == 1) fraudCount++;

        let rowClass = row["Prediction"] == 1 ? "fraud-row" : "";
        tableHTML += `<tr class="${rowClass}">`;

        keys.forEach(key => {
            tableHTML += `<td>${row[key]}</td>`;
        });

        tableHTML += "</tr>";
    });

    tableHTML += "</table></div>";

    // Summary Section
    const summaryHTML = `
        <div class="summary">
            <h3>📊 Prediction Summary</h3>
            <p><strong>Total Transactions:</strong> ${data.length}</p>
            <p><strong>Fraudulent Transactions:</strong> ${fraudCount}</p>
            <p><strong>Safe Transactions:</strong> ${data.length - fraudCount}</p>
        </div>
    `;

    document.getElementById("result").innerHTML = summaryHTML + tableHTML;
}
