// Affciher l'image téléchargée dans le champ d'aperçu
document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');

    imageUpload.addEventListener('change', function(event) {
        const [file] = event.target.files;
        if (file) {
            // Création d'une URL pour l'image téléchargée
            const imageUrl = URL.createObjectURL(file);
            imagePreview.src = imageUrl;  // Mettre à jour la source de l'image
            imagePreview.style.display = 'block';  // Afficher l'image
        }
    });
});


// Fonction pour mettre à jour la comboBox avec les options dynamiques
function updateTopOptions(options) {
    const comboBoxTop = document.getElementById("topResults");
    comboBoxTop.innerHTML = "";  // Vider les options existantes

    options.forEach(option => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.textContent = option;
        comboBoxTop.appendChild(opt);
    });
}

// Fonction pour appeler la vue 'affiche_top' via AJAX
function getTopOptions(fileName) {
    const apiUrl = '/api/affiche_top/';  // URL de l'API

    fetch(apiUrl + `?fileName=${fileName}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.options) {
            updateTopOptions(data.options);
        } else {
            console.error("Erreur : ", data.error);
        }
    })
    .catch(error => {
        console.error("Erreur lors de la requête AJAX :", error);
    });
}

// Fonction pour appeler la vue 'on_top_changed' via AJAX
function handleTopChange() {
    const selectedText = document.getElementById("topResults").value;

    const apiUrl = '/api/on_top_changed/';  // URL de l'API

    fetch(apiUrl + `?selected_text=${selectedText}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.sortie !== undefined) {
            console.log("Sortie :", data.sortie);  // Afficher la sortie (le nombre choisi)
        } else {
            console.error("Erreur :", data.error);
        }
    })
    .catch(error => {
        console.error("Erreur lors de la requête AJAX :", error);
    });
}

function chargerDescripteurs() {
    console.log('Chargement des descripteurs...');
    // TODO: appel au back-end (recherche.py)
}

function rechercher() {
    console.log('Recherche en cours...');
    // TODO: appel au back-end (recherche.py)
}

function afficherCourbe(type) {
    console.log('Affichage de la courbe :', type);
    // TODO: affichage de la courbe dans le canvas
}

function quitter() {
    window.close(); // ou redirection si besoin
}
