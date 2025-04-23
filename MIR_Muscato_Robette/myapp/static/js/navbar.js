fetch("/static/components/navbar.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("navbar-container").innerHTML = data;
        console.log("✅ Navbar Loaded Successfully");
        console.log(document.getElementById("navbar-container"));
        setActiveNavLink();
        // Réinitialiser les événements JavaScript après le chargement
        initializeNavbar();
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

document.addEventListener("DOMContentLoaded", function() {
    const navbarHTML = `
        <div class="navbar">
            <h1>Mon Projet MIR</h1>
            <div class="navbar-links">
                <a href="/">Accueil</a>
                <a href="/recherche/">Recherche</a>
                <a href="/profil/">Profil</a>
                <a href="/logout/">Déconnexion</a>
            </div>
        </div>
    `;
    document.getElementById("navbar-container").innerHTML = navbarHTML;
});
