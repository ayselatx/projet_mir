from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from .recherche_engine import Rechercheur
import pickle
from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from myapp.metriques import calculer_metriques
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔄 Redirection vers l'URL de redirection (paramètre ?next=/...), sinon vers 'home'
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            return redirect('home')  # Redirige vers la page d'accueil
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)  # Déconnecter l'utilisateur
    return redirect('login')  # Rediriger vers la page de connexion

def navbar_partial(request):
    return render(request, 'components/navbar.html')

@login_required
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

def get_races(request):
    animal = request.GET.get('animal')
    print("Animal:", animal)

    # Utilisation de MEDIA_ROOT pour définir le chemin correct
    base_dir = os.path.join(settings.MEDIA_ROOT, "MIR_DATASETS_B", animal)
    print("Base directory:", base_dir)

    if not os.path.exists(base_dir) or not os.path.isdir(base_dir):
        return JsonResponse({'races': []})

    races = [
        name for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
    ]
    return JsonResponse({'races': races})

def get_images(request):
    animal = request.GET.get('animal')
    race = request.GET.get('race')
    print("Animal:", animal)
    print("Race:",race)

    # Générer le chemin vers le dossier contenant les images
    base_dir = os.path.join(settings.MEDIA_ROOT, "MIR_DATASETS_B", animal, race)
    print("Base directory for images:", base_dir)


    if not os.path.exists(base_dir) or not os.path.isdir(base_dir):
        return JsonResponse({'images': []})

    # Liste des images dans le dossier
    images = [
        {
            'url': os.path.join(settings.MEDIA_URL, "MIR_DATASETS_B", animal, race, img),
            'name': img
        }
        for img in os.listdir(base_dir)
        if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))  # Filtrer les images
    ]
    
    return JsonResponse({'images': images})


def get_images_in_dataset(request):
    # Chemin du dossier des images
    dataset_path = os.path.join(settings.MEDIA_ROOT, 'MIR_DATASETS_CLIP')

    # Vérifier si le dossier existe
    if not os.path.exists(dataset_path):
        return JsonResponse({'error': 'Le dossier n\'existe pas.'}, status=400)

    # Liste des fichiers dans le dossier (images uniquement)
    images = []
    for f in os.listdir(dataset_path):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Créer l'URL complète pour chaque image
            image_url = os.path.join(settings.MEDIA_URL, 'MIR_DATASETS_CLIP', f)
            images.append({'url': image_url, 'name': f})
    print(images)

    # Renvoyer les images en réponse JSON
    return JsonResponse({'images': images})



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
    if 'undefined/undefined/' in file_name:
        options = ["Top 20", "Top 50", "Top 100"]
        return JsonResponse({'options': options})

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
        if not os.path.exists(dossier_racine):
            return JsonResponse({'error': f"Le dossier {dossier_racine} n'existe pas."}, status=400)

        for dossier_principal in os.listdir(dossier_racine):
            chemin_dossier_principal = os.path.join(dossier_racine, dossier_principal)  # Crée le chemin complet pour le dossier principal
            if os.path.isdir(chemin_dossier_principal):
                for dossier_animal in os.listdir(chemin_dossier_principal):  # Liste les dossiers dans chaque dossier principal
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
                "BGR": ("BGR", 'BGR'),
                "HSV": ("HSV", 'HSV'),
                "SIFT": ("SIFT", 'SIFT'),
                "ORB": ("ORB", 'ORB'),
                "GLCM": ("GLCM", 'GLCM'),
                "HOG": ("HOG", 'HOG'),
                "LBP": ("LBP", 'LBP'),
                "ViT": ("ViT", 'ViT'),
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
            
            
            # Sauvegarde les descripteurs dans un fichier .pkl
            features_pkl_path = os.path.join(settings.BASE_DIR, 'myapp', 'features.pkl')
            with open(features_pkl_path, 'wb') as f:
                pickle.dump(features, f)
            print(f"[✔] Chargement terminé : {len(features)} descripteurs chargés.")
            return JsonResponse({
                'features_count': len(features),
                'features': features
            })
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def recherche_images(request):
    if request.method == "POST":
        print("POST data:", request.POST)
        image_name = request.POST.get("image_name")
        text_query = request.POST.get("text_query", "").strip()
        search_type = request.POST.get("searchType", "").strip()
        combinaison_type = request.POST.get("combinaisonType", "").strip()
        distance_type = request.POST.get("distance", "").strip()
        top_results_str = request.POST.get("topResults", "20")
        top_results = int(top_results_str.split()[-1])  # garde "50" dans "Top 50"
        descripteurs = request.POST.get('descripteurs')
        if descripteurs:
            descripteurs_list = descripteurs.split(',')
        else:
            descripteurs_list = []
        print(image_name, text_query, search_type, combinaison_type, distance_type, top_results, descripteurs_list)
        if not image_name and not text_query:
            return JsonResponse({"error": "Aucune image ou texte fourni"}, status=400)
        rechercheur = Rechercheur()
        resultats = rechercheur.lancer_recherche(
            image_name=image_name,
            text_query=text_query,
            search_type=search_type,
            combination_type = combinaison_type,
            distance=distance_type,
            top_results=top_results,
            algo_choices=descripteurs
        )

        noms_resultats = []
        scores = []
        for (_, nom, score) in resultats:
            try:
                noms_resultats.append(str(nom))
                scores.append(float(score))
            except Exception as e:
                print(f"Erreur lors de l'extraction du nom : {e}")
        print('Noms des résultats :', noms_resultats)
        print('calcul des metriques...')
        if search_type != "clip":
            # Vérité terrain = même animal et race que l'image requête
            if text_query and not image_name:
                # On suppose que chaque résultat contient un score de similarité dans le tuple (score, nom, vecteur)
                cosine_moyenne = sum(scores) / len(scores) if scores else 0.0
                formatted_paths = [
                        "/media/MIR_DATASETS_B/" + nom.split("_")[2] + '/' + nom.split("_")[3] + '/' + nom.replace("\\", "/") for nom in noms_resultats
                    ]
                print(round(cosine_moyenne, 4))
                return JsonResponse({
                    "images": formatted_paths,
                    "cosine": round(cosine_moyenne, 4),
                })
            
            else : 
                try:
                    basename = os.path.basename(image_name)
                    race= basename.split("_")[3]
                    verite_terrain = race
                    print(f"Vérité terrain : {verite_terrain}")
                except Exception:
                    return JsonResponse({"error": "Format de nom d’image non valide"}, status=500)
                for nom in noms_resultats:
                    print(nom.split("_")[3])
                pertinents_recup = [1 if verite_terrain in nom.split("_")[3] else 0 for nom in noms_resultats]
                nb_pertinents = sum(pertinents_recup)
                dossier_racine = os.path.join(settings.MEDIA_ROOT, 'MIR_DATASETS_B')  # Utilise MEDIA_ROOT
                nb_images_pertinentes = 0
                if not os.path.exists(dossier_racine):
                    return JsonResponse({'error': f"Le dossier {dossier_racine} n'existe pas."}, status=400)

                for dossier_principal in os.listdir(dossier_racine):
                    chemin_dossier_principal = os.path.join(dossier_racine, dossier_principal)  # Crée le chemin complet pour le dossier principal
                    if os.path.isdir(chemin_dossier_principal):
                        for dossier_animal in os.listdir(chemin_dossier_principal):  # Liste les dossiers dans chaque dossier principal
                            # Vérifiez si le dossier animal correspond à la classe
                            if dossier_animal == verite_terrain:
                                chemin_dossier_race = os.path.join(chemin_dossier_principal, dossier_animal)  # Combine correctement les chemins
                                nb_images_pertinentes = len([f for f in os.listdir(chemin_dossier_race)
                                                            if os.path.isfile(os.path.join(chemin_dossier_race, f))])
                                break

                rappels = []
                precisions = []
                pertinents_cumules = 0

                for i, est_pertinent in enumerate(pertinents_recup):
                    if est_pertinent:
                        pertinents_cumules += 1
                    rappel = pertinents_cumules / nb_images_pertinentes
                    precision = pertinents_cumules / (i + 1)
                    print(f"Rappel: {rappel}, Précision: {precision}")
                    rappels.append(rappel)
                    precisions.append(precision)
                images_pertientes_recuperees = sum(pertinents_recup)
                images_recuperees = top_results
                print(f"Nombre d'images pertinentes récupérées : {images_pertientes_recuperees}")
                print(f"Nombre d'images récupérées : {images_recuperees}")
                print(f'Nombre d\'images pertinentes : {nb_images_pertinentes}')
                metriques = calculer_metriques(rappels, precisions, pertinents_recup, images_recuperees)
                # Format chemins
                formatted_paths = [
                        "/media/MIR_DATASETS_B/" + nom.split("_")[2] + '/' + nom.split("_")[3] + '/' + nom.replace("\\", "/") for nom in noms_resultats
                    ]


                return JsonResponse({
                    "images": formatted_paths,
                    "ap": metriques["ap"],
                    "map": metriques["map"],
                    "rp": metriques["rp"],
                    "rappels": rappels,
                    "precisions": precisions,
                })
        else:
            formatted_results = []
            if image_name and not text_query:
                # Requête image → descriptions
                # Trie les résultats par score décroissant
                resultats = sorted(resultats, key=lambda x: x[2], reverse=True)
                formatted_results = [{"description": nom, "score": round(score, 4)} for (_, nom, score) in resultats]
                return JsonResponse({
                    "descriptions": formatted_results,
                })

            elif text_query and not image_name:
                # Requête texte → images
                # Trie les résultats par score décroissant
                resultats = sorted(resultats, key=lambda x: x[2], reverse=True)
                formatted_paths = [
                    "/media/MIR_DATASETS_CLIP/" + nom for (_, nom, _) in resultats
                ]
                return JsonResponse({
                    "images": formatted_paths
                })
            else:
                return JsonResponse({"error": "Requête clip mal formée"}, status=400)


    return JsonResponse({"error": "Méthode non autorisée"}, status=405)





