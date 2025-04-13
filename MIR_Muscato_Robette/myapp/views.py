from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import numpy as np
import time
from .recherche_engine import Rechercheur
import pickle
from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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
    text_query = request.GET.get('textQuery', '')

    options = []

    if text_query and not file_name : 
        options = ["Top 20", "Top 50", "Top 100"]

    elif file_name or (file_name and text_query):
        filename_req = os.path.basename(file_name)  # Récupère juste le nom du fichier

        try:
            classe_image_requete = filename_req.split("_")[3]
        except IndexError:
            return JsonResponse({'error': f"Impossible d'extraire une classe depuis le nom {filename_req}"}, status=400)

        dossier_racine = os.path.join(settings.MEDIA_ROOT, 'MIR_DATASETS_B')  # Utilise MEDIA_ROOT
        nb_images_pertinentes = 0
        print(f'Dossier racine : {dossier_racine}')
        if not os.path.exists(dossier_racine):
            return JsonResponse({'error': f"Le dossier {dossier_racine} n'existe pas."}, status=400)

        for dossier_principal in os.listdir(dossier_racine):
            chemin_dossier_principal = os.path.join(dossier_racine, dossier_principal)  # Crée le chemin complet pour le dossier principal
            if os.path.isdir(chemin_dossier_principal):
                print(f'Dossier principal : {dossier_principal}')
                for dossier_animal in os.listdir(chemin_dossier_principal):  # Liste les dossiers dans chaque dossier principal
                    print(f'Dossier animal : {dossier_animal}')
                    # Vérifiez si le dossier animal correspond à la classe
                    if dossier_animal == classe_image_requete:
                        chemin_dossier_race = os.path.join(chemin_dossier_principal, dossier_animal)  # Combine correctement les chemins
                        nb_images_pertinentes = len([f for f in os.listdir(chemin_dossier_race)
                                                     if os.path.isfile(os.path.join(chemin_dossier_race, f))])
                        break

        print(f'Nombre d\'images pertinentes : {nb_images_pertinentes}')
        
        if nb_images_pertinentes >= 20:
            options.append("Top 20")
        if nb_images_pertinentes >= 50:
            options.append("Top 50")
        if nb_images_pertinentes >= 100:
            options.append("Top 100")

        options.append(f"Top {nb_images_pertinentes}")

    return JsonResponse({'options': options})


def affiche_distance(request):
    file_name = request.GET.get('fileName')
    descr = request.GET.get('descripteurs')

    print(file_name + ' et ' + descr)

    # Liste des options à retourner
    options = []  

    # Vérification de l'existence des descripteurs et de l'image
    if file_name and descr:
        descr_list = descr.split(",")  # Convertir la chaîne descripteurs en liste
        print(descr_list)

        # Groupes de descripteurs compatibles
        sift_orb_compatible = {'SIFT', 'ORB'}
        bgr_hsv_glcm_hog_lbp_vit_compatible = {'BGR', 'HSV', 'GLCM', 'HOG', 'LBP', 'ViT'}

        # Vérification de la compatibilité des descripteurs sélectionnés
        sift_orb_selected = any(d in descr_list for d in sift_orb_compatible)
        bgr_hsv_glcm_hog_lbp_vit_selected = any(d in descr_list for d in bgr_hsv_glcm_hog_lbp_vit_compatible)

        # Condition de compatibilité entre les groupes
        if sift_orb_selected and bgr_hsv_glcm_hog_lbp_vit_selected:
            return JsonResponse({'error': 'Veuillez choisir des descripteurs compatibles. SIFT/ORB ne peuvent pas être combinés avec BGR/HSV/GLCM/HOG/LBP/ViT.'})

        # Si le groupe SIFT/ORB est sélectionné, afficher les options associées
        if sift_orb_selected:
            options.append("Brute force")
            options.append("Flann")

        # Si le groupe BGR, HSV, GLCM, HOG, LBP, ViT est sélectionné, afficher les options associées
        if bgr_hsv_glcm_hog_lbp_vit_selected:
            options.append("Euclidienne")
            options.append("Correlation")
            options.append("Chi carré")
            options.append("Intersection")
            options.append("Bhattacharyya")

        # Ajouter des options supplémentaires si des descripteurs autres sont sélectionnés
        if any(descriptor in descr_list for descriptor in ['BGR', 'HSV', 'SIFT', 'ORB', 'GLCM', 'HOG', 'LBP', 'ViT']):
            options.append("Autres algos")

    else:
        return JsonResponse({'error': 'Veuillez fournir un nom de fichier et des descripteurs.'})

    # Retourner les options générées
    return JsonResponse({'options': options})



@csrf_exempt
def charger_descripteurs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            descripteurs = data.get('descripteurs', [])
            
            if not descripteurs:
                return JsonResponse({"error": "Aucun descripteur sélectionné."}, status=400)

            dossier_media = os.path.join(settings.MEDIA_ROOT)
            algo_map = {
                "BGR": ("BGR", 1),
                "HSV": ("HSV", 2),
                "SIFT": ("SIFT", 3),
                "ORB": ("ORB", 4),
                "GLCM": ("GLCM", 5),
                "HOG": ("HOG", 6),
                "LBP": ("LBP", 7),
                "ViT": ("ViT", 8),
            }

            folder_models = []
            algo_choices = []
            for d in descripteurs:
                if d in algo_map:
                    folder_models.append(os.path.join(dossier_media, algo_map[d][0]))
                    algo_choices.append(algo_map[d][1])

            if not folder_models:
                return JsonResponse({"error": "Aucun descripteur sélectionné."}, status=400)

            features = []
            total_files = sum([len(files) for folder in folder_models for _, _, files in os.walk(folder) if files])

            processed_files = 0
            for i, folder_model in enumerate(folder_models):
                if not os.path.exists(folder_model):
                    print('ici')
                    continue
                for root, _, files in os.walk(folder_model):
                    for file in files:
                        if not file.endswith('.txt'):
                            continue
                        feature_path = os.path.join(root, file)
                        try:
                            feature = np.loadtxt(feature_path).tolist()
                        except Exception as e:
                            continue
                        image_name = os.path.splitext(file)[0] + '.jpg'
                        image_path = os.path.join('media', image_name)
                        features.append({
                            'image': image_path,
                            'feature': feature,
                            'algo': algo_choices[i]
                        })

                        processed_files += 1
                        # Envoie la progression périodiquement (par exemple, toutes les 10 étapes)
                        if processed_files % 100 == 0:
                            progress = (processed_files / total_files) * 100
                            print(f"Progression: {progress:.2f}%")
            
            print(f"[✔] Chargement terminé : {len(features)} descripteurs chargés.")
            return JsonResponse({
                'features_count': len(features),
                'features': features
            })
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def recherche_images(request):
    print('Recherche demandée...')
    if request.method == "POST":
        # Récupérer les données du POST
        image_name = request.POST.get("image_name")
        text_query = request.POST.get("text_query", "").strip()
        search_type = request.POST.get("searchType", "").strip()
        distance_type = request.POST.get("distance", "").strip()
        top_results = request.POST.get("topResults", "").strip()

        print(f"Image: {image_name}, Texte: {text_query}")
        print(f"Type de recherche: {search_type}, Distance: {distance_type}, Top: {top_results}")

        if not image_name and not text_query:
            return JsonResponse({"error": "Aucune image ou texte fourni"}, status=400)

        # Tu peux caster top_results en int si besoin
        try:
            top_results = int(top_results.split(' ')[1])  # Extraire le nombre après "Top"
        except ValueError:
            top_results = 10  # valeur par défaut

        # Appelle ton moteur de recherche avec tous les paramètres
        rechercheur = Rechercheur()  # ton objet de recherche
        resultats = rechercheur.lancer_recherche(
            image_name=image_name,
            text_query=text_query,
            search_type=search_type,
            distance=distance_type,
            top_results=top_results
        )
        formatted_paths = []
        for result in resultats:
            filename = result[1]  # le deuxième élément du tuple
            parts = filename.split("_")
            if len(parts) >= 4:
                animal = parts[2]
                race = parts[3]
                path = "/media/MIR_DATASETS_B/" + str(animal) + '/' + str(race) + '/' + filename.replace("\\", "/")
                formatted_paths.append(path)

        return JsonResponse({"images": formatted_paths})


    return JsonResponse({"error": "Méthode non autorisée"}, status=405)




