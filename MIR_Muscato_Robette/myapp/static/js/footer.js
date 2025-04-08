fetch("/static/components/footer.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("footer-container").innerHTML = data;
        console.log("✅ Footer Loaded Successfully");
    })
    .catch(error => console.error("❌ Error loading footer:", error));
