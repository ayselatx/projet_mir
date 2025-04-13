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
function getTopOptions() {
    // Récupère l'image sélectionnée
    const selectedImage = document.querySelector('input[name="image_name"]:checked');  // Récupérer l'élément radio sélectionné
    const textQuery = document.getElementById("textQuery").value;  // Si un texte est aussi saisi
    let fileName = "";

    // Si une image est sélectionnée, on récupère son URL (chemin relatif uniquement)
    if (selectedImage) {
        const fullPath = selectedImage.value;
        //fileName = fullPath.split('/').slice(-3).join('/');  // Extraire le chemin relatif
        fileName = fullPath.split('/').pop();  // Récupère uniquement le nom du fichier
        splitName = fileName.split('_');
        fileName = splitName[2]+'/'+splitName[3]+'/'+fileName

    }

    const apiUrl = '/api/affiche_top/';  // L'URL de l'API qui va retourner les options top

    // On crée l'URL de la requête avec les paramètres
    let url = apiUrl + '?';

    if (fileName) {
        url += `fileName=${fileName}&`;  // Ajouter le paramètre de l'image
    }
    if (textQuery) {
        url += `textQuery=${encodeURIComponent(textQuery)}&`;  // Ajouter le paramètre du texte, si présent
    }

    // Retirer le dernier "&" de l'URL
    url = url.slice(0, -1);

    // Requête AJAX pour récupérer les options du top
    fetch(url, {
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

// Fonction pour mettre à jour les options du top dans le dropdown
function updateTopOptions(options) {
    const comboBoxTop = document.getElementById("topResults");
    comboBoxTop.innerHTML = "";  // On vide les options existantes

    options.forEach(option => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.textContent = option;
        comboBoxTop.appendChild(opt);
    });
}

// Ajouter un gestionnaire d'événements pour détecter les changements de sélection
document.querySelectorAll('input[name="image_name"]').forEach((radio) => {
    radio.addEventListener('change', getTopOptions);  // Écouter le changement de sélection d'image
});

// Ajouter un gestionnaire pour détecter le changement de texte (si nécessaire)
document.getElementById("textQuery").addEventListener("input", getTopOptions);

// Appel initial pour charger les options dès qu'une image ou un texte est sélectionné
getTopOptions();



// Fonction pour vérifier les conditions et afficher la liste des distances
function checkConditionsAndShowDistance() {
    const imageUploaded = document.querySelector('input[name="image_name"]:checked');
    const descripteursSelected = document.querySelectorAll("input[name='descripteur']:checked").length > 0;
    const comboBoxDistance = document.getElementById("distance");

    // Toujours afficher la liste déroulante
    comboBoxDistance.style.display = "block";
    comboBoxDistance.innerHTML = "";  // Vider les options précédentes

    if (imageUploaded && descripteursSelected) {
        getDistanceOptions();  // Appeler l’API pour charger les options
    } else {
        // Ajouter une seule option informative
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "Sélectionnez une image et un descripteur";
        comboBoxDistance.appendChild(opt);
    }
}


// Ajoutez un gestionnaire pour l'événement de téléchargement d'image
document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');

    imageUpload.addEventListener('change', function(event) {
        const [file] = event.target.files;
        if (file) {
            // Créer une URL pour l'image téléchargée et l'afficher
            const imageUrl = URL.createObjectURL(file);
            document.getElementById('imagePreview').src = imageUrl;
            document.getElementById('imagePreview').style.display = 'block';  // Afficher l'image
        }
        
        // Vérifier les conditions et mettre à jour la visibilité de la liste des distances
        checkConditionsAndShowDistance();
    });
});

// Ajouter un gestionnaire d'événements pour les descripteurs sélectionnés
document.querySelectorAll("input[name='descripteur']").forEach(function(checkbox) {
    checkbox.addEventListener('change', checkConditionsAndShowDistance);
});
// Fonction pour récupérer les options de distance via AJAX
function getDistanceOptions() {
    const selectedImage = document.querySelector('input[name="image_name"]:checked');
    let fileName = "";

    if (selectedImage) {
        const fullPath = selectedImage.value;
        fileName = fullPath.split('/').pop();  // Extraire le nom du fichier
        splitName = fileName.split('_');
        fileName = splitName[2] + '/' + splitName[3] + '/' + fileName;
    }

    const apiUrl = '/api/affiche_distance/';  // URL de l'API pour 'affiche_distance'

    // Créer l'URL de la requête avec le paramètre 'fileName'
    let url = apiUrl + '?fileName=' + encodeURIComponent(fileName);

    // Si des descripteurs sont sélectionnés, les ajouter à l'URL
    const descripteurs = [];
    document.querySelectorAll("input[name='descripteur']:checked").forEach(function(checkbox) {
        descripteurs.push(checkbox.value);
    });
    if (descripteurs.length > 0) {
        url += `&descripteurs=${descripteurs.join(",")}`;
    }

    // Requête AJAX pour récupérer les options de distance
    fetch(url, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Si une erreur est retournée dans le JSON, l'afficher à l'utilisateur
            alert(data.error);  // Afficher l'erreur dans une alerte
        } else if (data.options) {
            // Si les options sont présentes, mettre à jour l'interface
            updateDistanceOptions(data.options);
        } else {
            console.error("Erreur dans la réponse : Pas de 'options' dans le JSON");
        }
    })
    .catch(error => {
        console.error("Erreur lors de la requête AJAX :", error);
    });
}



// Fonction pour mettre à jour la comboBox avec les options de distance
function updateDistanceOptions(options) {
    const comboBoxDistance = document.getElementById("distance");
    comboBoxDistance.innerHTML = "";  // Vider les options existantes

    if (options && options.length > 0) {
        options.forEach(option => {
            const opt = document.createElement("option");
            opt.value = option;
            opt.textContent = option;
            comboBoxDistance.appendChild(opt);
        });
    } else {
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "Aucune option disponible";
        comboBoxDistance.appendChild(opt);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    const imageSelect = document.getElementById('imageSelect');
    const descripteursCheckboxes = document.querySelectorAll("input[name='descripteur']");
    
    imageSelect.addEventListener('change', checkConditionsAndShowDistance);
    descripteursCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', checkConditionsAndShowDistance);
    });

    // Vérifie si une image et des descripteurs ont été sélectionnés au chargement
    checkConditionsAndShowDistance();
});


function chargerDescripteurs() {
    // Récupère les descripteurs sélectionnés
    var descripteurs = [];
    document.querySelectorAll("input[name='descripteur']:checked").forEach(function(checkbox) {
        descripteurs.push(checkbox.value);
    });

    if (descripteurs.length === 0) {
        alert("Veuillez sélectionner au moins un descripteur.");
        return;
    }

    // Affiche la barre de progression et initialise la valeur
    document.getElementById('progressBar').value = 0;
    document.getElementById('progressPercent').innerText = '0%';

    // Envoie les données au serveur via AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/charger_descripteurs/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));  // Si tu utilises CSRF

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Quand la réponse est reçue, on met à jour la progression
            var response = JSON.parse(xhr.responseText);
            if (response.error) {
                alert(response.error);
            } else {
                console.log('Descripteurs chargés', response.features_count);
                // Mettre à jour l'interface avec les descripteurs chargés, si nécessaire.
            }
        }
    };

    // Envoi les descripteurs au serveur
    xhr.send(JSON.stringify({ 'descripteurs': descripteurs }));

    // Fonction pour vérifier régulièrement la progression (par exemple, toutes les 1 seconde)
    var interval = setInterval(function() {
        var progress = document.getElementById('progressBar').value;
        if (progress < 100) {
            document.getElementById('progressBar').value = progress + 1;
            document.getElementById('progressPercent').innerText = progress + 1 + '%';
        } else {
            clearInterval(interval);
        }
    }, 100);
}


// Fonction pour récupérer le token CSRF dans les cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function rechercher() {
    console.log('Recherche en cours...');

    // Récupérer les valeurs des champs
    const selectedImage = document.querySelector('input[name="image_name"]:checked');
    const textQuery = document.getElementById('textQuery').value;
    const searchType = document.getElementById('searchType').value; // Ajout de searchType
    const distanceType = document.getElementById('distance').value; // Ajout de distanceType
    const topResults = document.getElementById('topResults').value; // Ajout de topResults

    // Vérification si image ou texte est sélectionné
    if (!selectedImage && textQuery === "") {
        alert("Veuillez sélectionner une image ou insérer un texte.");
        return;
    }

    const csrfToken = getCookie('csrftoken');  // Récupérer le token CSRF

    // Création de FormData pour envoyer les données via POST
    const formData = new FormData();
    if (selectedImage) formData.append("image_name", selectedImage.value); // Image
    if (textQuery !== "") formData.append("text_query", textQuery); // Texte
    formData.append("searchType", searchType);  // Type de recherche
    formData.append("distance", distanceType);  // Type de distance
    formData.append("topResults", topResults);  // Nombre de résultats à retourner

    try {
        const response = await fetch("/recherche_images/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        });

        const data = await response.json();
        console.log(data);
        
        // Affichage des résultats
        if (data.images && data.images.length > 0) {
            afficherResultats(data.images);
        } else {
            document.getElementById('results').innerHTML = '<p>Aucun résultat trouvé.</p>';
        }
    } catch (error) {
        console.error("Erreur lors de la recherche :", error);
        alert("Une erreur est survenue.");
    }
}



// Fonction pour afficher les résultats dans la section #results
function afficherResultats(images) {
    console.log('afficher les resultats')
    console.log(images)
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';  // Réinitialiser les résultats existants
    images.forEach(image => {
        const imgElement = document.createElement('img');
        imgElement.src = image;
        imgElement.alt = "Résultat de recherche";
        imgElement.classList.add("thumbnail");  // Classe CSS pour les vignettes d'images
        resultsContainer.appendChild(imgElement);
    });
}




function afficherCourbe(type) {
    console.log('Affichage de la courbe :', type);
    // TODO: affichage de la courbe dans le canvas
}

function quitter() {
    window.close(); // ou redirection si besoin
}
