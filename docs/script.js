document.getElementById("claim-form").onsubmit = async function (e) {
  e.preventDefault();

  const input = document.getElementById("claim-input").value;
  const output = document.getElementById("output");
  output.textContent = "Analyzing claim. Please wait...";

  try {
    const res = await fetch("https://your-api-url/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ claim: input })
    });

    const data = await res.json();

    let resultText = "";

    if (data.summary) {
      resultText += "Summary:\n" + data.summary + "\n\n";
    }

    if (data.flags && Array.isArray(data.flags) && data.flags.length > 0) {
      resultText += "Flags:\n" + data.flags.join("\n") + "\n\n";
    }

    if (typeof data.score === "number") {
      resultText += "Confidence Score: " + (data.score * 100).toFixed(1) + "%\n\n";
    }

    if (data.response) {
      resultText += "Full Response:\n" + data.response;
    } else if (!resultText) {
      resultText = "No meaningful output returned from analysis.";
    }

    output.textContent = resultText;

  } catch (err) {
    output.textContent = "Error: Failed to contact the backend or parse the response.";
    console.error(err);
  }
};
