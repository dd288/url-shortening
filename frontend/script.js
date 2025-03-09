const API_BASE_URL = "http://127.0.0.1:8000/api/";  // Update if needed

async function shortenUrl() {
    const longUrl = document.getElementById("longUrl").value.trim();
    if (!longUrl) {
        alert("Please enter a valid URL.");
        return;
    }

    try {
        const response = await fetch(API_BASE_URL + "shorten/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ long_url: longUrl })
        });

        const data = await response.json();
        if (response.ok) {
            const shortUrl = data.short_url;   // The backend already provides the correct full URL
            console.log("✅ Final Short URL:", shortUrl);
            document.getElementById("shortUrlOutput").innerHTML = `Short URL: <a href="${shortUrl}" target="_blank">${shortUrl}</a>`;
        } else {
            document.getElementById("shortUrlOutput").innerText = `Error: ${data.detail || "Failed to shorten URL"}`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("shortUrlOutput").innerText = "Failed to connect to the server.";
    }
}

async function retrieveUrl() {
    let shortUrl = document.getElementById("shortUrl").value.trim();
    if (!shortUrl) {
        alert("Please enter a short URL.");
        return;
    }

    // Extract only the short code (last part of the URL)
    const urlParts = shortUrl.split("/");
    const shortCode = urlParts[urlParts.length - 1] || urlParts[urlParts.length - 2];

    try {
        const response = await fetch(API_BASE_URL + `retrieve/?short_url=${shortCode}`);

        const data = await response.json();
        if (response.ok) {
            document.getElementById("originalUrlOutput").innerHTML = `Original URL: <a href="${data.long_url}" target="_blank">${data.long_url}</a>`;
        } else {
            document.getElementById("originalUrlOutput").innerText = `Error: ${data.detail || "Short URL not found"}`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("originalUrlOutput").innerText = "Failed to connect to the server.";
    }
}
