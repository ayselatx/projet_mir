document.addEventListener("DOMContentLoaded", function () {
    const datasetSelect = document.getElementById("datasetSelect");
    const descripteursSection = document.getElementById("descripteursSection");
    const distanceContainer = document.getElementById("distanceContainer");
    const metriquesTexteSection = document.getElementById("metriquesTexteSection");
    const metriquesClipSection = document.getElementById("metriquesClipSection");
    const searchTypeDiv = document.getElementById("searchType");
    const clipTextResult = document.getElementById("clipTextResult");
    const combinationTypeContainer = document.getElementById("combinationTypeContainer");

    function updateInterfaceVisibility() {
        const selectedDataset = datasetSelect.value;
        const isClip = selectedDataset === "MIR_DATASETS_CLIP";

        // Descripteurs & distances
        descripteursSection.style.display = isClip ? 'none' : 'block';
        distanceContainer.style.display = isClip ? 'none' : 'block';

        // Métriques
        metriquesClipSection.style.display = isClip ? 'block' : 'none';
        metriquesTexteSection.style.display = isClip ? 'none' : 'block';

        // Résultats texte
        clipTextResult.style.display = isClip ? "block" : "none";

        // Mise à jour des checkboxes selon dataset
        if (isClip) {
            searchTypeDiv.innerHTML = `
                <label>
                    <input type="checkbox" name="searchType" value="clip" class="search-type-checkbox">
                    CLIP
                </label>
            `;
        } else if (selectedDataset) {
            searchTypeDiv.innerHTML = `
                <label>
                    <input type="checkbox" name="searchType" value="image" class="search-type-checkbox">
                    Image
                </label><br>
                <label>
                    <input type="checkbox" name="searchType" value="texte" class="search-type-checkbox">
                    Texte
                </label>
            `;
        } else {
        // Aucun dataset sélectionné => proposer image + texte + clip
        searchTypeDiv.innerHTML = `
            <label>
                <input type="checkbox" name="searchType" value="image" class="search-type-checkbox">
                Image
            </label><br>
            <label>
                <input type="checkbox" name="searchType" value="texte" class="search-type-checkbox">
                Texte
            </label><br>
            <label>
                <input type="checkbox" name="searchType" value="clip" class="search-type-checkbox">
                CLIP
            </label>
        `;
    }


        // Attacher les événements après ajout dynamique
        attachSearchTypeListeners();
        updateCombinationTypeVisibility();
    }

    function attachSearchTypeListeners() {
        const checkboxes = document.querySelectorAll(".search-type-checkbox");
        checkboxes.forEach(cb => {
            cb.addEventListener("change", updateCombinationTypeVisibility);
        });
    }

    function updateCombinationTypeVisibility() {
        const checkboxes = document.querySelectorAll(".search-type-checkbox");
        const checkedValues = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        const hasImage = checkedValues.includes("image");
        const hasText = checkedValues.includes("texte");
        const hasClip = checkedValues.includes("clip");

        // Gestion affichage combinaison métriques
        const metriquesImageSection = document.getElementById("metriquesImageSection");

        if (hasClip && !hasImage && !hasText) {
            // CLIP seul
            metriquesClipSection.style.display = "block";
            metriquesTexteSection.style.display = "none";
            metriquesImageSection.style.display = "block";

        } else if (hasText && !hasImage) {
            // Texte seul
            metriquesTexteSection.style.display = "block";
            metriquesClipSection.style.display = "none";
            metriquesImageSection.style.display = "none";

        } else if (hasImage && !hasText) {
            // Image seul
            metriquesImageSection.style.display = "block";
            metriquesTexteSection.style.display = "none";
            metriquesClipSection.style.display = "none";

        } else if (hasImage && hasText) {
            // Image + Texte
            metriquesImageSection.style.display = "block";
            metriquesTexteSection.style.display = "none";
            metriquesClipSection.style.display = "none";

        } else {
            // Aucun ou autre combinaison
            metriquesImageSection.style.display = "none";
            metriquesTexteSection.style.display = "none";
            metriquesClipSection.style.display = "none";
        }

        // Affichage du combo seulement si Image + Texte coché
        if (hasImage && hasText) {
            combinationTypeContainer.style.display = "block";
        } else {
            combinationTypeContainer.style.display = "none";
        }
    }


    // Initial setup
    datasetSelect.addEventListener("change", updateInterfaceVisibility);
    updateInterfaceVisibility(); // Au chargement
});




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

                // Création du wrapper pour la vignette d'image et le bouton radio
                const wrapper = document.createElement('div');
                wrapper.classList.add('image-wrapper');

                // Crée l'input radio
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = 'image_name';
                radio.value = img.url;
                radio.addEventListener('change', getTopOptions); // Ajoute l'événement pour changer l'image sélectionnée

                // Crée l'image (vignette)
                const imageElement = document.createElement('img');
                imageElement.src = img.url;
                imageElement.alt = img.name;
                imageElement.classList.add('image-preview');  // Même classe que pour les résultats

                // Ajoute le radio et l'image dans le wrapper
                wrapper.appendChild(radio);
                wrapper.appendChild(imageElement);

                // Ajout du wrapper à la prévisualisation
                imagePreview.appendChild(wrapper);
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


function updateImagePreview() {
    const imageSelect = document.getElementById('imageSelect');
    const imagePreview = document.getElementById('imagePreview');
    const selectedImage = imageSelect.value;

    imagePreview.innerHTML = ''; // Nettoyer l'affichage existant

    if (selectedImage) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('image-wrapper');  // même classe que pour les résultats

        const imgElement = document.createElement('img');
        imgElement.src = selectedImage;
        imgElement.alt = "Vignette de l'image sélectionnée";
        imgElement.classList.add("image-preview");  // même classe que pour les résultats

        wrapper.appendChild(imgElement);
        imagePreview.appendChild(wrapper);
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
    console.log('ICI');

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
        console.log("Champs dans la réponse :", Object.keys(data));

        // Réinitialiser les conteneurs
        document.getElementById("clipTextResult").innerHTML = "";
        document.getElementById("results").innerHTML = "";

        if (data.images && data.images.length > 0) {
            const searchType = Array.from(document.querySelectorAll("input[name='searchType']:checked")).map(checkbox => checkbox.value)[0];
            console.log("Type de recherche sélectionné :", searchType);

            if (searchType === 'clip'){
                afficherResultatsCLIP(data.images, data.scores);
                // Affiche automatiquement les courbes après les résultats
                afficherCourbe("rappel", "courbeRappel");
                afficherCourbe("precision", "courbePrecision");}
            else {
            
                afficherResultats(data.images, data.scores);;
            }

            if ("ap" in data && "map" in data && "rp" in data) {
                document.getElementById("cosine").textContent = "0.0";
                document.getElementById("apValue").textContent = data.ap.toFixed(4);
                document.getElementById("mapValue").textContent = data.map.toFixed(4);
                document.getElementById("rpValue").textContent = data.rp.toFixed(4);
                window.rappels = data.rappels;
                window.precisions = data.precisions;
                // Affiche automatiquement les courbes après les résultats
                afficherCourbe("rappel", "courbeRappel");
                afficherCourbe("precision", "courbePrecision");


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
            document.getElementById("apValue").textContent = data.ap.toFixed(4);
            document.getElementById("mapValue").textContent = data.map.toFixed(4);
            document.getElementById("rpValue").textContent = data.rp.toFixed(4);
            window.rappels = data.rappels;
            window.precisions = data.precisions;
            afficherCourbe("rappel", "courbeRappel");
            afficherCourbe("precision", "courbePrecision");

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

function nettoyerClésCaptions(captions) {
    const cleanedCaptions = {};
    for (const key in captions) {
        const cleanedKey = key.replace(/\s+/g, '');
        cleanedCaptions[cleanedKey] = captions[key];
    }
    return cleanedCaptions;
}


async function afficherResultats(images, scores) {
    console.log("Début de l'affichage des résultats");

    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

        const response = await fetch('/media/captions.json');
        const rawCaptions = await response.json();
        const captions = nettoyerClésCaptions(rawCaptions);
        console.log('Captions nettoyées :', captions);


        images.forEach((imageUrl, index)=> {
            const score = scores[index]; // Récupère le score associé à l'image

            console.log('Traitement de l\'image :', imageUrl);

            const wrapper = document.createElement('div');
            wrapper.classList.add('image-wrapper');

            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.alt = "Résultat de recherche";
            imgElement.classList.add("image-preview");

            // Récupération du chemin relatif à partir de "media/"
            const relativePath = imageUrl.replace(/^.*?media\//, '').replace(/^MIR_DATASETS_B\//, '');
            console.log('Chemin relatif utilisé :', relativePath);

            const captionText = captions[relativePath];

            const descElement = document.createElement('p');
            descElement.classList.add('image-description');
            descElement.textContent = captionText || 'Aucune description disponible';

            const scoreElement = document.createElement('p');
            scoreElement.classList.add('image-score');
            scoreElement.textContent = `Score : ${score.toFixed(4)}`;

            wrapper.appendChild(imgElement);
            wrapper.appendChild(descElement);
            wrapper.appendChild(scoreElement);

            resultsContainer.appendChild(wrapper);
        });
    console.log("Affichage terminé");
}





async function afficherResultatsCLIP(images, scores) {
    console.log('afficher les resultats');
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    // Charger et parser le fichier CSV avec séparateur |
    const response = await fetch('/media/results.csv');
    const csvText = await response.text();
    const descriptions = parseCSV(csvText);

    images.forEach((imageUrl, index)  => {

        const score = scores[index]; // Récupère le score associé à l'image

        const imageName = imageUrl.split('/').pop(); // Extrait le nom du fichier (ex. "1000092795.jpg")
        const matchingEntry = descriptions.find(entry =>
            entry.image_name === imageName && entry.comment_number === '0'
        );

        const wrapper = document.createElement('div');
        wrapper.classList.add('image-wrapper');

        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.alt = "Résultat de recherche";
        imgElement.classList.add("image-preview");

        wrapper.appendChild(imgElement);

        if (matchingEntry) {
            const descElement = document.createElement('p');
            descElement.classList.add('image-description');
            descElement.textContent = matchingEntry.comment;
            wrapper.appendChild(descElement);
        }

        const scoreElement = document.createElement('p');
        scoreElement.classList.add('image-score');
        scoreElement.textContent = `Score : ${score.toFixed(4)}`;
        
        wrapper.appendChild(scoreElement);

        resultsContainer.appendChild(wrapper);
    });
}

// Fonction de parsing CSV avec séparateur "|"
function parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split('|').map(h => h.trim());

    return lines.slice(1).map(line => {
        const values = line.split('|').map(v => v.trim());
        const entry = {};
        headers.forEach((header, index) => {
            entry[header] = values[index];
        });
        return entry;
    });
}


let chartInstances = {};

function afficherCourbe(type, canvasId) {
    if (!window.rappels || !window.precisions) {
        console.error("Les valeurs de rappel et précision ne sont pas disponibles.");
        return;
    }

    const labels = Array.from({ length: window.rappels.length }, (_, index) => index + 1);
    const data = (type === 'rappel') ? window.rappels : window.precisions;
    const labelText = (type === 'rappel') ? "Rappel" : "Précision";
    const color = (type === 'rappel') ? "rgb(54, 162, 235)" : "rgb(255, 99, 132)";

    const ctx = document.getElementById(canvasId).getContext("2d");

    // Détruire l'ancienne instance si elle existe
    if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
    }

    // Créer et stocker une nouvelle instance
    chartInstances[canvasId] = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: labelText,
                data: data,
                borderColor: color,
                backgroundColor: color,
                fill: false,
                tension: 0.2,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Indice de l'image",
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: labelText,
                    }
                }
            }
        }
    });
}


function telechargerGraphique(canvasId, nomFichier) {
    const canvas = document.getElementById(canvasId);
    const image = canvas.toDataURL("image/png");

    const link = document.createElement('a');
    link.href = image;
    link.download = nomFichier;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
    const imageSelect = document.getElementById('imageSelect');
    const imagePreview = document.getElementById('imagePreview');
    const sectionAnimalRace = document.getElementById('sectionAnimalRace');
    const sectionImageTexte = document.getElementById('sectionImageTexte');
    const chargementMessage = document.getElementById('chargementImagesMessage');

    let imagesCache = null; // ✅ Déclaré en dehors de l'écouteur pour le cache

    sectionAnimalRace.style.display = 'block';
    sectionImageTexte.style.display = 'block';

    datasetSelect.addEventListener('change', function () {
        console.log("🧠 Changement détecté !");
        const selectedValue = datasetSelect.value;

                if (selectedValue === 'MIR_DATASETS_CLIP') {
                    if (imagesCache) {
                        console.log('Utilisation des images en cache:', imagesCache);
                        updateImagePreview(imagesCache); // Fonction à créer pour réutiliser ce bloc d'affichage
                        return;
                    }

                    chargementMessage.innerText = "Chargement des images...";

                    fetch('/get_images_in_dataset/')
                        .then(response => response.json())
                        .then(data => {
                            console.log('Images récupérées:', data.images);
                            imagesCache = data.images;

                            // Réinitialiser le sélecteur et les vignettes
                            imageSelect.innerHTML = '<option value="">-- Sélectionnez une image --</option>';
                            imagePreview.innerHTML = '';

                            let promises = [];

                            data.images.forEach(img => {
                            const opt = document.createElement('option');
                            opt.value = img.url;
                            opt.textContent = img.name;
                            imageSelect.appendChild(opt);

                            // Création du wrapper
                            const wrapper = document.createElement('div');
                            wrapper.classList.add('image-wrapper');

                            // Création du label contenant input + image
                            const label = document.createElement('label');
                            label.className = 'image-option';
                            
                            // Ajout du input et image dans le label
                            const input = document.createElement('input');
                            input.type = 'radio';
                            input.name = 'image_name';
                            input.value = img.url;
                            input.addEventListener('change', getTopOptions);

                            const imageElement = document.createElement('img');
                            imageElement.src = img.url;
                            imageElement.alt = img.name;
                            imageElement.classList.add('image-preview');

                            label.appendChild(input);
                            label.appendChild(imageElement);

                            // Ajout du label au wrapper
                            wrapper.appendChild(label);

                            // Ajout du wrapper à l'imagePreview
                            imagePreview.appendChild(wrapper);

                            // Promesse de chargement d’image
                            let imageLoadPromise = new Promise((resolve, reject) => {
                                const imgElement = new Image();
                                imgElement.src = img.url;
                                imgElement.onload = () => resolve(img.url);
                                imgElement.onerror = () => reject(`Erreur lors du chargement de l'image : ${img.url}`);
                            });

                            promises.push(imageLoadPromise);
                        });


                            Promise.all(promises)
                                .then(() => {
                                    chargementMessage.innerText = "Images chargées.";
                                    imageSelect.disabled = false;
                                })
                                .catch(error => {
                                    console.error(error);
                                    chargementMessage.innerText = "Erreur lors du chargement des images.";
                                });
                        })
                        .catch(error => {
                            console.error('Erreur lors de la récupération des images:', error);
                            chargementMessage.innerText = "Erreur lors du chargement des images.";
                        });

                    sectionAnimalRace.style.display = 'none';
                    sectionImageTexte.style.display = 'block';
                    checkbox_descripteurs.style.display = 'none';
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


