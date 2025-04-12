from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings


# Create your views here.
def home(request):
    # Chemin vers le dossier des images
    dataset_path = os.path.join(settings.MEDIA_ROOT, 'datasets/MIR_DATASETS_B')

    # Vérifie si le dossier existe et affiche un message de débogage
    if not os.path.exists(dataset_path):
        print(f"Le dossier n'existe pas : {dataset_path}")
        images = []  # Si le dossier n'existe pas, on passe une liste vide
    else:
        print(f"Le dossier existe : {dataset_path}")  # Affiche si le dossier existe

        images = []
        
        # Parcours le dossier et ses sous-dossiers
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                # Si le fichier est une image, on l'ajoute à la liste
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Filtre les types d'image
                    # Ajoute le chemin relatif de l'image dans le dossier 'datasets/MIR_DATASETS_B'
                    image_path = os.path.relpath(os.path.join(root, file), dataset_path)
                    images.append(image_path)

        # Débogue : affiche la liste des fichiers trouvés
        print(f"Fichiers trouvés dans le dossier : {images}")

    # Passe la liste des images et MEDIA_URL au template
    return render(request, 'home.html', {'images': images, 'MEDIA_URL': settings.MEDIA_URL})


def indexation(request):
    return render(request, "indexation.html",{})

def recherche(request):

    images = []

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Récupère le chemin relatif à MEDIA_ROOT
                relative_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
                # Normalise le chemin pour usage web (remplace les \ par /)
                images.append(relative_path.replace('\\', '/'))

    context = {
        'images': images,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, "recherche.html",context)


def on_top_changed(request):
    selected_text = request.GET.get('selected_text', '')
    if selected_text:
        try:
            sortie = int(selected_text.split(' ')[1])  # Extraire le nombre
            return JsonResponse({'sortie': sortie})
        except ValueError:
            return JsonResponse({'error': 'Le format du texte sélectionné est invalide'}, status=400)
    return JsonResponse({'error': 'Aucun texte sélectionné'}, status=400)

def affiche_top(request):
    file_name = request.GET.get('fileName', '')

    # Nettoyer la comboBox et ajouter seulement les options valides
    options = []
    
    if not file_name:
        options = ["Top 20", "Top 50", "Top 100"]
    else:
        filename_req = os.path.basename(file_name)
        try:
            classe_image_requete = filename_req.split("_")[3]
        except IndexError:
            return JsonResponse({'error': f"Impossible d'extraire une classe depuis le nom {filename_req}"}, status=400)

        # Chercher le nombre d'images pertinentes
        dossier_racine = "MIR_DATASETS_B"
        nb_images_pertinentes = 0

        for dossier_principal in os.listdir(dossier_racine):
            chemin_dossier_principal = os.path.join(dossier_racine, dossier_principal)
            if os.path.isdir(chemin_dossier_principal):
                for dossier_race in os.listdir(chemin_dossier_principal):
                    if dossier_race == classe_image_requete:
                        chemin_dossier_race = os.path.join(dossier_racine, dossier_principal, dossier_race)
                        nb_images_pertinentes = len([f for f in os.listdir(chemin_dossier_race)
                                                     if os.path.isfile(os.path.join(chemin_dossier_race, f))])
                        break

        if nb_images_pertinentes >= 20:
            options.append("Top 20")
        if nb_images_pertinentes >= 50:
            options.append("Top 50")
        if nb_images_pertinentes >= 100:
            options.append("Top 100")
        
        options.append(f"Top {nb_images_pertinentes}")

    return JsonResponse({'options': options})
