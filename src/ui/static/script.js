// Dark/Light mode toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("theme-toggle");
  const html = document.documentElement;

  const applyTheme = (theme) => {
    html.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  };

  // Set initial theme
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme) {
    applyTheme(storedTheme);
  } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    applyTheme("dark");
  }

  toggle?.addEventListener("click", () => {
    const current =
      html.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(current);
  });
});

// Claim form handler
document.getElementById("claim-form").onsubmit = async function (e) {
  e.preventDefault();

  const inputField = document.getElementById("claim-input");
  const output = document.getElementById("output");
  const submitButton = this.querySelector("button");

  const input = inputField.value.trim();
  if (!input) {
    output.textContent = "Please enter a claim.";
    return;
  }

  output.textContent = "Analyzing claim. Please wait...";
  submitButton.disabled = true;

  const BASE_URL =
    location.hostname === "localhost" || location.hostname === "127.0.0.1"
      ? "http://localhost:5000"
      : "https://claimforge-api.onrender.com";

  try {
    const res = await fetch(`${BASE_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ claim: input }),
    });

    if (!res.ok) {
      throw new Error(`Server responded with status ${res.status}`);
    }

    const data = await res.json();
    let resultText = "";

    if (data.summary) {
      resultText += `Summary:\n${data.summary}\n\n`;
    }

    if (Array.isArray(data.flags) && data.flags.length > 0) {
      resultText += `Flags:\n${data.flags.join("\n")}\n\n`;
    }

    if (typeof data.score === "number") {
      resultText += `Confidence Score: ${(data.score * 100).toFixed(1)}%\n\n`;
    }

    if (data.response) {
      resultText += `Full Response:\n${data.response}`;
    }

    if (!resultText) {
      resultText = "No meaningful output returned from analysis.";
    }

    output.textContent = resultText;
  } catch (err) {
    console.error("Error:", err);
    output.textContent =
      "❌ Error: Unable to reach backend or process response.";
  } finally {
    submitButton.disabled = false;
  }
};
