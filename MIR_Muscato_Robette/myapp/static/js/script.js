
document.getElementById('animalSelect').addEventListener('change', function () {
    const animal = this.value;
    const raceSelect = document.getElementById('raceSelect');
    raceSelect.innerHTML = '<option value="">Chargement...</option>';
    raceSelect.disabled = true;

    fetch(`/get_races/?animal=${animal}`)
        .then(res => res.json())
        .then(data => {
            raceSelect.innerHTML = '<option value="">-- Sélectionnez une race --</option>';
            data.races.forEach(race => {
                const opt = document.createElement('option');
                opt.value = race;
                opt.textContent = race;
                raceSelect.appendChild(opt);
            });
            raceSelect.disabled = false;
        });
});

document.getElementById('raceSelect').addEventListener('change', function () {
    const animal = document.getElementById('animalSelect').value;
    const race = this.value;
    const imageSelect = document.getElementById('imageSelect');
    const imagePreview = document.getElementById('imagePreview');
    const chargementMessage = document.getElementById('chargementImagesMessage');  // Message de chargement

    // Affiche le message de chargement
    chargementMessage.innerText = "Chargement des images...";
    
    // Désactive le sélecteur et vide la preview
    imageSelect.innerHTML = '<option value="">Chargement...</option>';
    imageSelect.disabled = true;
    imagePreview.innerHTML = '';

    fetch(`/get_images/?animal=${animal}&race=${race}`)
        .then(res => res.json())
        .then(data => {
            // Réinitialisation du sélecteur
            imageSelect.innerHTML = '<option value="">-- Sélectionnez une image --</option>';
            
            // Ajout des options d'image au sélecteur
            data.images.forEach(img => {
                const opt = document.createElement('option');
                opt.value = img.url;
                opt.textContent = img.name;
                imageSelect.appendChild(opt);

                // Création de la vignette d'image
                const label = document.createElement('label');
                label.className = 'image-option';
                label.innerHTML = `
                    <input type="radio" name="image_name" value="${img.url}">
                    <img src="${img.url}" alt="${img.name}" class="thumbnail">
                `;
                imagePreview.appendChild(label);

                // Ajout de l'événement sur le radio
                const lastInput = label.querySelector('input[type="radio"]');
                lastInput.addEventListener('change', getTopOptions);
            });

            // Réactive le sélecteur une fois les images chargées
            imageSelect.disabled = false;

            // Mise à jour du message de chargement une fois les images chargées
            chargementMessage.innerText = "Images chargées.";
        })
        .catch(error => {
            // Affiche un message d'erreur si la requête échoue
            chargementMessage.innerText = "Erreur lors du chargement des images.";
            console.error("Erreur lors du chargement des images :", error);
        });
});


// Fonction pour mettre à jour la vignette en fonction de la sélection de l'image
function updateImagePreview() {
    const imageSelect = document.getElementById('imageSelect');
    const imagePreview = document.getElementById('imagePreview');
    const selectedImage = imageSelect.value;
    // Si une image est sélectionnée, on affiche la vignette
    if (selectedImage) {
        // Crée une nouvelle image de prévisualisation
        const imgElement = document.createElement('img');
        imgElement.src = selectedImage; // Utilise l'URL de l'image sélectionnée
        imgElement.alt = "Vignette de l'image sélectionnée";
        imgElement.classList.add("thumbnail");  // Classe CSS pour les vignettes d'images

        // Vider le conteneur de prévisualisation pour éviter d'afficher plusieurs images
        imagePreview.innerHTML = '';
        imagePreview.appendChild(imgElement);  // Ajouter la vignette à l'affichage
    } else {
        // Si aucune image n'est sélectionnée, vider la prévisualisation
        imagePreview.innerHTML = '';
    }
}


// Fonction pour appeler la vue 'affiche_top' via AJAX
function getTopOptions(selectedImage,textQuery) {
    // Récupère l'image sélectionnée
    let fileName = "";

    // Si une image est sélectionnée, on récupère son URL (chemin relatif uniquement)
    if (selectedImage) {
        const fullPath = selectedImage.value;
        //fileName = fullPath.split('/').slice(-3).join('/');  // Extraire le chemin relatif
        fileName = fullPath.split('\\').pop();  // Récupère uniquement le nom du fichier
        splitName = fileName.split('_');
        fileName = splitName[2]+'/'+splitName[3]+'/'+fileName

    }

    const apiUrl = '/api/affiche_top/';  // L'URL de l'API qui va retourner les options top

    // On crée l'URL de la requête avec les paramètres
    let url = apiUrl + '?';
    console.log("fileName:", fileName)
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



// Fonction pour vérifier les conditions et afficher la liste des distances
function checkConditionsAndShowDistance() {
    const imageSelect = document.getElementById('imageSelect');
    const imagePreview = document.getElementById('imagePreview');
    const descripteursSelected = document.querySelectorAll("input[name='descripteur']:checked").length > 0;
    const comboBoxDistance = document.getElementById("distance");

    // Toujours afficher la liste déroulante
    comboBoxDistance.style.display = "block";
    comboBoxDistance.innerHTML = "";  // Vider les options précédentes

    if ((imageSelect || imagePreview) && descripteursSelected) {
        getDistanceOptions();  // Appeler l’API pour charger les options
    } else {
        // Ajouter une seule option informative
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "Sélectionnez une image et un descripteur";
        comboBoxDistance.appendChild(opt);
    }
}

// Ajouter un gestionnaire d'événements pour les descripteurs sélectionnés
document.querySelectorAll("input[name='descripteur']").forEach(function(checkbox) {
    checkbox.addEventListener('change', checkConditionsAndShowDistance);
});
// Fonction pour récupérer les options de distance via AJAX
function getDistanceOptions() {
    const imageSelect = document.getElementById('imageSelect');
    const imagePreview = document.getElementById('imagePreview');
    let fileName = "";

    if (imageSelect) {
        const fullPath = imageSelect.value;
        fileName = fullPath.split('/').pop();  // Extraire le nom du fichier
        splitName = fileName.split('_');
        fileName = splitName[2] + '/' + splitName[3] + '/' + fileName;
    }
    if (imagePreview.value != undefined) {
        const fullPath = imagePreview.value;
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

    // Affiche le message de chargement
    var messageEl = document.getElementById('chargementMessage');
    messageEl.innerText = "Chargement en cours...";

    // Affiche la barre de progression et initialise la valeur
    document.getElementById('progressBar').value = 0;
    document.getElementById('progressPercent').innerText = '0%';

    // Envoie les données au serveur via AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/charger_descripteurs/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));  // CSRF token

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.error) {
                    alert(response.error);
                    messageEl.innerText = "Erreur lors du chargement.";
                } else {
                    console.log('Descripteurs chargés', response.features_count);
                    messageEl.innerText = "Chargement terminé.";
                    // Mettre à jour l'interface ici si besoin
                }
            } else {
                messageEl.innerText = "Erreur serveur.";
            }
        }
    };

    // Envoie les descripteurs au serveur
    xhr.send(JSON.stringify({ 'descripteurs': descripteurs }));

    // Simulation de progression (à adapter si tu peux envoyer une vraie progression côté serveur)
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

// Exemple de fonction qui récupère les vraies valeurs depuis l'API ou les résultats
async function rechercher() {
    console.log('Recherche en cours...');

    // Affiche le message de recherche en cours
    const messageEl = document.getElementById('rechercheMessage');
    messageEl.innerText = "Recherche en cours...";
    const messageElText = document.getElementById('rechercheMessageText');
    messageElText.innerText = "Recherche en cours...";

    // Récupérer les valeurs des champs
    let selectedImage = document.querySelector('input[name="image_name"]:checked');
    if (!selectedImage) {
        const dropdown = document.getElementById("imageSelect");
        if (dropdown && dropdown.value) {
            selectedImage = { value: dropdown.value };
        }
    }
    const textQuery = document.getElementById('textQuery').value;
    const searchType = Array.from(document.querySelectorAll("input[name='searchType']:checked")).map(checkbox => checkbox.value);
    const combinaisonType = document.getElementById('combinationType').value;
    const distanceType = document.getElementById('distance').value;
    const topResults = document.getElementById('topResults').value;

    console.log('combinaisonType:', combinaisonType);
    console.log('searchType:', searchType);

    if (searchType.length === 0) {
        alert("Veuillez sélectionner un type de recherche");
        messageEl.innerText = "";
        return;
    }

    const descripteurs = [];
    document.querySelectorAll("input[name='descripteur']:checked").forEach(function(checkbox) {
        descripteurs.push(checkbox.value);
    });

    if (!selectedImage && textQuery === "") {
        alert("Veuillez sélectionner une image ou insérer un texte.");
        messageEl.innerText = "";
        return;
    }

    const csrfToken = getCookie('csrftoken');

    const formData = new FormData();
    if (selectedImage) formData.append("image_name", selectedImage.value);
    if (textQuery !== "") formData.append("text_query", textQuery);
    formData.append("searchType", searchType);
    formData.append("combinaisonType", combinaisonType);
    formData.append("distance", distanceType);
    formData.append("topResults", topResults);
    if (descripteurs.length > 0) {
        formData.append("descripteurs", descripteurs.join(","));
    }

    try {
        const response = await fetch("/recherche_images/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        });

        const data = await response.json();

        // Réinitialiser les conteneurs
        document.getElementById("clipTextResult").innerHTML = "";
        document.getElementById("results").innerHTML = "";

        if (data.images && data.images.length > 0) {
            afficherResultats(data.images);

            if ("ap" in data && "map" in data && "rp" in data) {
                document.getElementById("cosine").textContent = "0.0";
                document.getElementById("apValue").textContent = data.ap.toFixed(4);
                document.getElementById("mapValue").textContent = data.map.toFixed(4);
                document.getElementById("rpValue").textContent = data.rp.toFixed(4);
                window.rappels = data.rappels;
                window.precisions = data.precisions;
            } else if ("cosine" in data) {
                document.getElementById("cosine").textContent = data.cosine.toFixed(4);
                document.getElementById("apValue").textContent = "0.0";
                document.getElementById("mapValue").textContent = "0.0";
                document.getElementById("rpValue").textContent = "0.0";
                window.rappels = [];
                window.precisions = [];
            }
        } else if (data.descriptions && data.descriptions.length > 0) {
            const clipTextContainer = document.getElementById("clipTextResult");
            clipTextContainer.innerHTML = "<h4>Descriptions trouvées :</h4><ul></ul>";
            const ul = clipTextContainer.querySelector("ul");

            let totalScore = 0;

            data.descriptions.forEach(item => {
                const li = document.createElement("li");
                li.textContent = `${item.description} (score: ${item.score.toFixed(4)})`;
                ul.appendChild(li);
                totalScore += item.score;
            });

            const moyenneScore = (totalScore / data.descriptions.length).toFixed(4);
            document.getElementById("score").textContent = moyenneScore;

            document.getElementById("cosine").textContent = data.cosine?.toFixed(4) || "0.0";
            document.getElementById("apValue").textContent = "0.0";
            document.getElementById("mapValue").textContent = "0.0";
            document.getElementById("rpValue").textContent = "0.0";
            window.rappels = [];
            window.precisions = [];

            document.getElementById("results").innerHTML = "";
        } else {
            document.getElementById('results').innerHTML = '<p>Aucun résultat trouvé.</p>';
            document.getElementById("clipTextResult").innerHTML = "";
        }

        messageEl.innerText = "Recherche terminée.";
    } catch (error) {
        console.error("Erreur lors de la recherche :", error);
        alert("Une erreur est survenue.");
        messageEl.innerText = "Erreur lors de la recherche.";
    }
}





// Fonction pour afficher les résultats dans la section #results
function afficherResultats(images) {
    console.log('afficher les resultats')
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

let chartInstance = null; // Pour réutiliser le même graphique

// Fonction pour afficher la courbe de rappel ou de précision
function afficherCourbe(type) {
    // Vérification que les valeurs sont disponibles
    if (!window.rappels || !window.precisions) {
        console.error("Les valeurs de rappel et précision ne sont pas disponibles.");
        return;
    }

    // Utilisation des indices comme étiquettes de l'axe des X (nombre d'images)
    const labels = Array.from({ length: window.rappels.length }, (_, index) => index + 1);  // Indices des images (1, 2, 3, ..., n)
    
    // Sélectionner les bonnes données en fonction du type (rappel ou précision)
    const data = (type === 'rappel') ? window.rappels : window.precisions;
    const labelText = (type === 'rappel') ? "Rappel" : "Précision";
    const color = (type === 'rappel') ? "rgb(54, 162, 235)" : "rgb(255, 99, 132)";

    const ctx = document.getElementById("courbeRP").getContext("2d");

    // Si un graphique existe déjà, on le détruit
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Création du graphique avec Chart.js
    chartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,  // Les indices des images comme labels de l'axe X
            datasets: [{
                label: labelText,
                data: data,  // Les valeurs de rappel ou de précision sur l'axe Y
                borderColor: color,
                backgroundColor: color,
                fill: false,
                tension: 0.2,
            }],
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Indice de l'image",  // Le titre de l'axe X
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: type === 'rappel' ? "Rappel" : "Précision",  // Le titre de l'axe Y
                    }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const imageSelect = document.getElementById('imageSelect');
    // 1. Quand on change la sélection dans le menu déroulant
    imageSelect.addEventListener('change', (event) => {
        updateImagePreview();   // Met à jour la preview
        getTopOptions(imageSelect,undefined);        // Met à jour les options du top
    });
    // 2. Quand on tape dans le champ de sélection (si applicable)
    imageSelect.addEventListener('input', getTopOptions);
    // 3. Quand on change de sélection via les radios (image_name)
    document.querySelectorAll('input[name="image_name"]').forEach((radio) => {
        radio.addEventListener('change', getTopOptions);
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const imageSelect = document.getElementById('imagePreview');

    // Écouteur sur le conteneur (délégation d'événement)
    imageSelect.addEventListener('change', (event) => {
        const target = event.target;
        // Vérifie si c'est une radio avec le bon name
        if (target && target.name === 'image_name' && target.type === 'radio') {
            imageSelect.value = target.value;
            getTopOptions(target,undefined);
        }
    });
});

document.getElementById("textQuery").addEventListener("input", (event) => {
    const textQuery = event.target.value;

    // Vérifie si les options sont déjà présentes dans le DOM
    const optionsContainer = document.getElementById("topResults")  // Remplace par l'élément qui contient les options
    if (optionsContainer && optionsContainer.children.length > 0) {
        console.log("Options déjà présentes, pas de mise à jour.");
        return;  // On arrête l'exécution si les options sont déjà présentes
    }

    // Sinon, on met à jour
    getTopOptions(undefined, textQuery);
});

document.addEventListener('DOMContentLoaded', () => {
    // Sélectionne les deux éléments imageSelect et imagePreview
    const imageSelect = document.getElementById('imageSelect');
    
    // Sélectionne toutes les cases à cocher des descripteurs
    const descripteursCheckboxes = document.querySelectorAll("input[name='descripteur']");
    
    // Ajout des écouteurs d'événements pour imageSelect et imagePreview
    imageSelect.addEventListener('change', checkConditionsAndShowDistance);
    
    // Ajout des écouteurs d'événements pour les checkboxes des descripteurs
    descripteursCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', checkConditionsAndShowDistance);
    });
    checkConditionsAndShowDistance();
});

document.addEventListener('DOMContentLoaded', () => {
    // Sélectionne les deux éléments imageSelect et imagePreview
    const imagePreview = document.getElementById('imagePreview');
    
    // Sélectionne toutes les cases à cocher des descripteurs
    const descripteursCheckboxes = document.querySelectorAll("input[name='descripteur']");
    
    // Ajout des écouteurs d'événements pour imageSelect et imagePreview
    imagePreview.addEventListener('change', checkConditionsAndShowDistance);
    
    // Ajout des écouteurs d'événements pour les checkboxes des descripteurs
    descripteursCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', checkConditionsAndShowDistance);
    });
    checkConditionsAndShowDistance();
});

document.querySelectorAll("input[name='searchType']").forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        const selectedTypes = Array.from(document.querySelectorAll("input[name='searchType']:checked"))
            .map(cb => cb.value);

        const hasImage = selectedTypes.includes("image");
        const hasTexte = selectedTypes.includes("texte");

        const combinationContainer = document.getElementById('combinationTypeContainer');
        combinationContainer.style.display = (hasImage && hasTexte) ? 'block' : 'none';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const datasetSelect = document.getElementById('datasetSelect');
    const imageSelect = document.getElementById('imageSelect'); // Le sélecteur d'image
    const imagePreview = document.getElementById('imagePreview'); // Conteneur des vignettes
    const sectionAnimalRace = document.getElementById('sectionAnimalRace');
    const sectionImageTexte = document.getElementById('sectionImageTexte');
    const chargementMessage = document.getElementById('chargementImagesMessage');  // Ajout du message de chargement

    sectionAnimalRace.style.display = 'block';
    sectionImageTexte.style.display = 'block';

    datasetSelect.addEventListener('change', function() {
        console.log("🧠 Changement détecté !");
        const selectedValue = datasetSelect.value;
        
        if (selectedValue === 'MIR_DATASETS_CLIP') {
            // Afficher un message de chargement pendant la récupération des images
            chargementMessage.innerText = "Chargement des images...";

            fetch('/get_images_in_dataset/')
                .then(response => response.json())
                .then(data => {
                    console.log('Images récupérées:', data.images);
                    
                    // Vider les options existantes du sélecteur d'images et les vignettes
                    imageSelect.innerHTML = '<option value="">-- Sélectionnez une image --</option>';
                    imagePreview.innerHTML = ''; // Vider les vignettes

                    let promises = []; // Créer un tableau pour les promesses

                    // Ajouter les nouvelles options dans le sélecteur d'images et les vignettes
                    data.images.forEach(img => {
                        // Ajouter l'option dans le sélecteur déroulant
                        const opt = document.createElement('option');
                        opt.value = img.url;
                        console.log("img.url:", img.url)
                        opt.textContent = img.name;
                        imageSelect.appendChild(opt);

                        // Ajouter la vignette à la section des images disponibles
                        const label = document.createElement('label');
                        label.className = 'image-option';
                        label.innerHTML = `
                            <input type="radio" name="image_name" value="${img.url}">
                            <img src="${img.url}" alt="${img.name}" class="thumbnail">
                        `;
                        imagePreview.appendChild(label);

                        const lastInput = label.querySelector('input[type="radio"]');
                        lastInput.addEventListener('change', getTopOptions);

                        // Ajouter une promesse pour chaque image (requête de chargement de l'image)
                        let imageLoadPromise = new Promise((resolve, reject) => {
                            const imgElement = new Image();
                            imgElement.src = img.url;
                            imgElement.onload = () => resolve(img.url);  // Résoudre la promesse quand l'image est chargée
                            imgElement.onerror = () => reject(`Erreur lors du chargement de l'image : ${img.url}`);  // Rejeter la promesse si erreur
                        });

                        promises.push(imageLoadPromise); // Ajouter la promesse à notre tableau
                    });

                    // Attendre que toutes les images soient chargées avant de modifier le message
                    Promise.all(promises)
                        .then(() => {
                            chargementMessage.innerText = "Images chargées.";  // Message à afficher quand toutes les images sont prêtes
                            imageSelect.disabled = false;  // Activer le sélecteur d'images
                        })
                        .catch((error) => {
                            console.error(error);
                            chargementMessage.innerText = "Erreur lors du chargement des images.";  // Message d'erreur si une image échoue
                        });
                })
                .catch(error => {
                    console.error('Erreur lors de la récupération des images:', error);
                    chargementMessage.innerText = "Erreur lors du chargement des images.";  // Message en cas d'erreur avec fetch
                });

            // Masquer ou afficher les sections en fonction de la sélection du dataset
            sectionAnimalRace.style.display = 'none';
            sectionImageTexte.style.display = 'block';
        } else {
            console.log("Autre dataset sélectionné :", selectedValue);
            sectionAnimalRace.style.display = 'block';
            sectionImageTexte.style.display = 'block';
        }
    });
});







function quitter() {
    window.close(); // ou redirection si besoin
}


