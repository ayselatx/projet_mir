fetch("/static/components/navbar.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("navbar-container").innerHTML = data;

        setActiveNavLink();
    });

function setActiveNavLink() {
    let currentPage = window.location.pathname.split("/").pop(); 
    console.log("Current Page:", currentPage);

    let navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPage) {
            link.classList.add("actif"); 
            console.log(" Active Class Added:", link);

        } else {
            link.classList.remove("actif");
        }
    });
}
