#Defintion de toute les fonctions Ã  appeller dans l'interface
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
import cv2
import numpy as np
from skimage.transform import resize
from skimage import exposure
from skimage import io, color, img_as_ubyte
from matplotlib import pyplot as pltimport 
from PIL import Image 
import operator, math, os, glob 
# import torch.nn as nn 
from matplotlib.pyplot import imread as pyimread
from skimage.feature import greycomatrix, greycoprops, local_binary_pattern
import time
import json
from sentence_transformers import SentenceTransformer
import pickle
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

def showDialog():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Merci de sÃ©lectionner un descripteur via le menu ci-dessus")
    msgBox.setWindowTitle("Pas de Descripteur sÃ©lectionnÃ©")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    returnValue = msgBox.exec()

def generateHistogramme_Color(filenames, progressBar):
    start = time.time()
    if not os.path.isdir("BGR"):
        os.mkdir("BGR")
    
    # Compter le nombre total d'images pour la barre de progression
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    i = 0
    for root, _, files in os.walk(filenames):  # Parcours rï¿½cursif des sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vï¿½rifier les extensions
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)
                #img = cv2.resize(img, (64,128))

                if img is None:
                    print(f"Impossible de lire {img_path}, image ignoree.")
                    continue  # Passer ï¿½ l'image suivante si erreur        img = cv2.imread(filenames+"/"+path)
                histB = cv2.calcHist([img],[0],None,[256],[0,256])
                histG = cv2.calcHist([img],[1],None,[256],[0,256])
                histR = cv2.calcHist([img],[2],None,[256],[0,256])
                        
                feature = np.hstack((histB.ravel(), histG.ravel(), histR.ravel()))


                num_image = os.path.splitext(file)[0]
                np.savetxt("BGR/"+str(num_image)+".txt" ,feature)
                
                # Mise a jour de la barre de progression
                i += 1
                progressBar.setValue(int(100 * (i / total_images)))
                
    print(f"Indexation Hist Couleur (BGR) terminee en {time.time() - start:.2f} secondes !!!")


def generateHistogramme_HSV(filenames, progressBar):
    import time
    start = time.time()
    
    # Crï¿½er le dossier s'il n'existe pas
    if not os.path.isdir("HSV"):
        os.mkdir("HSV")

    # Compter le nombre total d'images pour la barre de progression
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    i = 0
    for root, _, files in os.walk(filenames):  # Parcours rï¿½cursif des sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vï¿½rifier les extensions
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)
                #img = cv2.resize(img, (64,128))

                if img is None:
                    print(f"Impossible de lire {img_path}, image ignoree.")
                    continue  # Passer ï¿½ l'image suivante si erreur

                # Convertir en HSV et calculer les histogrammes
                img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                histH = cv2.calcHist([img_hsv], [0], None, [180], [0, 180])
                histS = cv2.calcHist([img_hsv], [1], None, [256], [0, 256])
                histV = cv2.calcHist([img_hsv], [2], None, [256], [0, 256])

                # Concatï¿½ner les histogrammes
                feature = np.hstack((histH.ravel(), histS.ravel(), histV.ravel()))

                # Sauvegarde dans un fichier
                num_image = os.path.splitext(file)[0]
                np.savetxt(f"HSV/{num_image}.txt", feature)

                # Mise ï¿½ jour de la barre de progression
                i += 1
                progressBar.setValue(int(100 * (i / total_images)))

    print(f"Indexation Hist HSV terminee en {time.time() - start:.2f} secondes !!!")

def generateHistogramme_HOG(filenames, progressBar):
    start = time.time()
    
    # Créer le dossier HOG s'il n'existe pas
    if not os.path.isdir("HOG"):
        os.mkdir("HOG")

    # Compter le nombre total d'images pour la barre de progression
    total_images = sum(1 for _, _, files in os.walk(filenames) 
                        for f in files if f.lower().endswith((".jpg", ".jpeg", ".png")))
    
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    # Création du descripteur HOG avec des paramètres standard
    win_size = (64, 128)  # Taille standard pour HOG
    block_size = (16, 16)
    block_stride = (8, 8)
    cell_size = (8, 8)
    nbins = 9

    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)

    i = 0

    for root, _, files in os.walk(filenames):  # Parcours récursif des dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vérifier les extensions
                img_path = os.path.join(root, file)
                
                # Lire l'image en niveaux de gris
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (64,128))
                if img is None:
                    print(f"Impossible de lire {img_path}, image ignoree.")
                    continue  # Passer à l'image suivante

                # Redimensionner à la taille attendue par HOG
                #img = resize_and_pad(img, (64, 128))  # Resize while keeping aspect ratio

                # Extraire les caractéristiques HOG
                feature = hog.compute(img)
                
                # Vérifier que le descripteur est bien généré
                if feature is None or feature.shape[0] == 0:
                    print(f"Erreur : HOG non calcule pour {img_path}")
                    continue

                # Sauvegarder les caractéristiques sous forme de fichier texte
                num_image = os.path.splitext(file)[0]
                np.savetxt(f"HOG/{num_image}.txt", feature.ravel())

                # Mettre à jour la barre de progression
                progressBar.setValue(int(100 * (i + 1) / total_images))
                i += 1

    print(f"Indexation HOG terminee en {time.time() - start:.2f} secondes !")

def generateSIFT(filenames, progressBar):
    start = time.time()
    
    # Crï¿½er le rï¿½pertoire SIFT s'il n'existe pas dï¿½jï¿½
    if not os.path.isdir("SIFT"):
        os.mkdir("SIFT")

    # Compter le nombre total d'images
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
    
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    i = 0
    for root, _, files in os.walk(filenames):  # Traverse tous les sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vï¿½rifie le format de l'image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lit en niveau de gris
                img = cv2.resize(img, (64,128))

                if img is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                sift = cv2.SIFT_create(nfeatures=2000)  # SIFT avec 2000 features max
                key_points, descriptors = sift.detectAndCompute(img, None)

                if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouvï¿½s
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"SIFT/{num_image}.txt", descriptors)
                else:
                    print(f"Aucun descripteur trouve pour {file} donc essaye d'augmente le contrast")
                    # Convertir l'image en niveaux de gris si ce n'est pas dï¿½jï¿½ fait
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
                    
                    # Appliquer CLAHE pour amï¿½liorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)
                    key_points, descriptors = sift.detectAndCompute(enhanced_img, None)
                    
                    if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouvï¿½s
                        num_image = os.path.splitext(file)[0]
                        np.savetxt(f"SIFT/{num_image}.txt", descriptors)
                        print(f"ca a fonctionner pour {file}")
                    else:
                        print(f"Aucun descripteur trouve pour {file}")


                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise ï¿½ jour correcte de la barre de progression

    print(f"Indexation SIFT terminee en {time.time() - start:.2f} secondes !!!!")
    
def generateORB(filenames, progressBar):
    start = time.time()
    
    # Crï¿½er le rï¿½pertoire SIFT s'il n'existe pas dï¿½jï¿½
    if not os.path.isdir("ORB"):
        os.mkdir("ORB")

    # Compter le nombre total d'images
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
    
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    i = 0
    for root, _, files in os.walk(filenames):  # Traverse tous les sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vï¿½rifie le format de l'image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lit en niveau de gris
                #img = cv2.resize(img, (64,128))
                
                if img is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                sift = cv2.ORB_create(nfeatures=2000)  # SIFT avec 2000 features max
                key_points, descriptors = sift.detectAndCompute(img, None)

                if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouvï¿½s
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"ORB/{num_image}.txt", descriptors)
                else:
                    print(f"Aucun descripteur trouve pour {file} donc essaye d'augmente le contrast")
                    # Convertir l'image en niveaux de gris si ce n'est pas dï¿½jï¿½ fait
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
                    
                    # Appliquer CLAHE pour amï¿½liorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)
                    key_points, descriptors = sift.detectAndCompute(enhanced_img, None)
                    
                    if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouvï¿½s
                        num_image = os.path.splitext(file)[0]
                        np.savetxt(f"ORB/{num_image}.txt", descriptors)
                        print(f"ca a fonctionner pour {file}")
                    else:
                        print(f"Aucun descripteur trouve pour {file}")


                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise ï¿½ jour correcte de la barre de progression

    print(f"Indexation ORB terminee en {time.time() - start:.2f} secondes !!!!")

    
def generateGLCM(filenames, progressBar): 
    start = time.time()
    
    # Crï¿½er le dossier GLCM s'il n'existe pas
    if not os.path.isdir("GLCM"): 
        os.mkdir("GLCM") 

    distances = [1, -1]  
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]  

    # Compter le nombre total d'images pour la barre de progression
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
    
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    i = 0  
    for root, _, files in os.walk(filenames):  # Traverse tous les sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vï¿½rifier format image
                img_path = os.path.join(root, file)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lire en niveaux de gris
                #image = cv2.resize(image, (64,128))
                if image is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                # Convertir en format appropriï¿½ pour GLCM
                gray = img_as_ubyte(image)  

                # Calculer la matrice GLCM
                glcm_matrix = greycomatrix(gray, distances=distances, angles=angles, normed=True)

                # Extraire les propriï¿½tï¿½s GLCM
                features = []
                for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
                    features.extend(greycoprops(glcm_matrix, prop).ravel())

                feature_vector = np.array(features)

                if len(feature_vector) > 0:  # Vï¿½rifier que descripteurs trouvï¿½s
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"GLCM/{num_image}.txt", feature_vector)
                else:
                    print(f"Aucun descripteur trouve pour {file}, augmentation du contraste...")

                    # Appliquer CLAHE pour amï¿½liorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)

                    # Recalculer la GLCM avec l'image amï¿½liorï¿½e
                    glcm_matrix = greycomatrix(enhanced_img, distances=distances, angles=angles, normed=True)
                    
                    features = []
                    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
                        features.extend(greycoprops(glcm_matrix, prop).ravel())

                    feature_vector = np.array(features)

                    if len(feature_vector) > 0:  # Sauvegarde si amï¿½lioration rï¿½ussie
                        np.savetxt(f"GLCM/{num_image}.txt", feature_vector)
                        print(f"Amelioration reussie pour {file} !")
                    else:
                        print(f"Echec de l'amelioration pour {file}")

                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise ï¿½ jour de la barre de progression

    print(f"Indexation GLCM terminee en {time.time() - start:.2f} secondes !!!!")
    

def generateLBP(filenames, progressBar): 
    start = time.time()
    # Create LBP directory if it doesn't exist
    if not os.path.isdir("LBP"): 
        os.mkdir("LBP") 

    points = 8  
    radius = 1  
    method = 'default'  
    subSize = (70, 70)  

    # Count total images for progress tracking
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))

    if total_images == 0:
        print("No images found!")
        return

    i = 0  
    for root, _, files in os.walk(filenames):  # Recursive folder traversal
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)

                if img is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (350, 350))

                fullLBPmatrix = local_binary_pattern(img, points, radius, method)
                histograms = []

                for k in range(int(fullLBPmatrix.shape[0] / subSize[0])): 
                    for j in range(int(fullLBPmatrix.shape[1] / subSize[1])): 
                        subVector = fullLBPmatrix[k * subSize[0]:(k + 1) * subSize[0], j * subSize[1]:(j + 1) * subSize[1]].ravel()
                        subHist, _ = np.histogram(subVector, bins=int(2**points), range=(0, 2**points))
                        histograms = np.concatenate((histograms, subHist), axis=None)

                if len(histograms) > 0:  
                    num_image, _ = os.path.splitext(file)
                    np.savetxt(f"LBP/{num_image}.txt", histograms)
                else:
                    print(f"Aucun descripteur trouve pour {file}, augmentation du contraste...")
                    
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(img)

                    fullLBPmatrix = local_binary_pattern(enhanced_img, points, radius, method)
                    histograms = []

                    for k in range(int(fullLBPmatrix.shape[0] / subSize[0])): 
                        for j in range(int(fullLBPmatrix.shape[1] / subSize[1])): 
                            subVector = fullLBPmatrix[k * subSize[0]:(k + 1) * subSize[0], j * subSize[1]:(j + 1) * subSize[1]].ravel()
                            subHist, _ = np.histogram(subVector, bins=int(2**points), range=(0, 2**points))
                            histograms = np.concatenate((histograms, subHist), axis=None)

                    if len(histograms) > 0:  
                        np.savetxt(f"LBP/{num_image}.txt", histograms)
                        print(f"Amelioration reussie pour {file} !")
                    else:
                        print(f"Echec de l'amelioration pour {file}")

                i += 1
                progressBar.setValue(int(100 * (i / total_images)))
    print(f"Indexation GLCM terminee en {time.time() - start:.2f} secondes !!!!")


def embedding_text(progressBar, input_file="captions.json", output_text_file="text_embeddings_LLM.pkl"):
    try:
        print("Début du traitement des descriptions textuelles...")

        # Charger le fichier contenant les descriptions textuelles
        with open(input_file, "r") as f:
            descriptions = json.load(f)
            print("Fichier JSON chargé")

        if not descriptions:
            print("Le fichier JSON est vide.")
            if progressBar:
                progressBar.setValue(100)
            return

        # Charger le modèle Sentence Transformer
        text_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

        # Transformer les descriptions en embeddings avec mise à jour de la barre
        print("Génération des embeddings textuels...")
        text_embeddings = {}
        total_texts = len(descriptions)

        for i, (img, desc) in enumerate(descriptions.items()):
            text_embeddings[img] = text_model.encode(desc)
            if progressBar:
                progressBar.setValue(int((i + 1) / total_texts * 100))  # Mise à jour de la barre de progression (100%)

        # Sauvegarde des embeddings textuels
        with open(output_text_file, "wb") as f:
            pickle.dump(text_embeddings, f)
        print(f"Embeddings textuels sauvegardés dans {output_text_file}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} est introuvable.")
        if progressBar:
            progressBar.setValue(100)
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {input_file} n'est pas un JSON valide.")
        if progressBar:
            progressBar.setValue(100)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        if progressBar:
            progressBar.setValue(100)


def embedding_image(filenames, progressBar, output_image_file="image_embeddings_VIT.pkl"):
    try:
        print("Début du traitement des images...")

        # Charger un modèle pré-entraîné pour extraire les features des images
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        image_model = models.vit_b_16(pretrained=True)  # Vision Transformer large (384 dimensions)
        image_model.heads = torch.nn.Identity()  # Supprimer la dernière couche de classification
        image_model = image_model.to(device)
        image_model.eval()

        # Définir les transformations pour prétraiter les images
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        image_embeddings = {}

        # Récupérer la liste des fichiers images
        image_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(filenames)
            for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        total_images = len(image_files)

        if total_images == 0:
            print("Aucun fichier image trouvé.")
            if progressBar:
                progressBar.setValue(100)
            return

        # Extraction des embeddings des images avec mise à jour de la barre
        for i, img_path in enumerate(image_files):
            file_name = os.path.basename(img_path)
            try:
                # Charger et transformer l'image
                image = Image.open(img_path).convert("RGB")
                image = transform(image).unsqueeze(0).to(device)

                # Extraire les features
                with torch.no_grad():
                    embedding = image_model(image).cpu().numpy().flatten()

                # Sauvegarder l'embedding
                image_embeddings[file_name] = embedding

            except Exception as e:
                print(f"Erreur avec {file_name} : {e}")

            if progressBar:
                progressBar.setValue(int((i + 1) / total_images * 100))  # Mise à jour de la barre (60% max pour les images)

        # Sauvegarde des embeddings d'images
        with open(output_image_file, "wb") as f:
            pickle.dump(image_embeddings, f)

        print(f"Embeddings d'images sauvegardés dans {output_image_file}")

    except FileNotFoundError:
        print(f"Erreur : Le dossier {filenames} est introuvable.")
        if progressBar:
            progressBar.setValue(100)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        if progressBar:
            progressBar.setValue(100)

def embedding_imageCLIP(folder_path, progressBar, output_image_file="image_embeddings_CLIP.pkl", output_text_file="text_embeddings_CLIP.pkl", captions_file="captions.json"):
    try:
        print("Chargement du modèle CLIP...")
        model = SentenceTransformer('clip-ViT-B-32')
        model.eval()

        # --------- TRAITEMENT DES IMAGES ---------
        print("Début du traitement des images...")

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        image_embeddings = {}

        # Récupération des fichiers image dans le dossier
        image_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(folder_path)
            for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        total_images = len(image_files)

        if total_images == 0:
            print("Aucune image trouvée dans le dossier.")
            if progressBar:
                progressBar.setValue(100)
            return

        for i, img_path in enumerate(image_files):
            file_name = os.path.basename(img_path)
            try:
                image = Image.open(img_path).convert("RGB")

                # Extraire les embeddings avec CLIP
                with torch.no_grad():
                    embedding = model.encode([image])[0]

                image_embeddings[file_name] = embedding

            except Exception as e:
                print(f"Erreur lors du traitement de l'image {file_name} : {e}")

            if progressBar:
                progressBar.setValue(int((i + 1) / (total_images + 1) * 50))  # Barre à 50% max pour images

        # Sauvegarde des embeddings d’images
        with open(output_image_file, "wb") as f:
            pickle.dump(image_embeddings, f)

        print(f"Embeddings d’images sauvegardés dans {output_image_file}")

        # --------- TRAITEMENT DES DESCRIPTIONS TEXTUELLES ---------
        print("Début du traitement des descriptions textuelles...")

        with open(captions_file, "r", encoding="utf-8") as f:
            descriptions = json.load(f)

        if not descriptions:
            print("Fichier captions.json vide.")
            if progressBar:
                progressBar.setValue(100)
            return

        text_embeddings = {}
        total_texts = len(descriptions)

        for i, (img_name, desc) in enumerate(descriptions.items()):
            try:
                embedding = model.encode(desc)
                text_embeddings[img_name] = embedding
            except Exception as e:
                print(f"Erreur lors de l'encodage du texte pour {img_name} : {e}")

            if progressBar:
                progressBar.setValue(50 + int((i + 1) / total_texts * 50))  # Mise à jour barre de 50% à 100%

        with open(output_text_file, "wb") as f:
            pickle.dump(text_embeddings, f)

        print(f"Embeddings textuels sauvegardés dans {output_text_file}")

    except FileNotFoundError as fnf_error:
        print(f"Erreur : {fnf_error}")
        if progressBar:
            progressBar.setValue(100)
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {captions_file} n'est pas un JSON valide.")
        if progressBar:
            progressBar.setValue(100)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        if progressBar:
            progressBar.setValue(100)





def search_by_text_CLIP():
    # Charger les embeddings des images et des textes depuis les fichiers pkl
    with open('/content/image_embeddings_CLIP.pkl', 'rb') as f:
        image_embeddings = pickle.load(f)

    # Convertir les embeddings en numpy arrays
    image_embeddings = np.array([embedding.cpu().numpy() if embedding.is_cuda else embedding.numpy() for embedding in image_embeddings.values()])

    with open('/content/text_embeddings_CLIP.pkl', 'rb') as f:
    text_embeddings = pickle.load(f)
    # Convertir les embeddings en numpy arrays
    text_embeddings = np.array([embedding.cpu().numpy() if embedding.is_cuda else embedding.numpy() for embedding in text_embeddings.values()])
    print(text_embeddings.shape)  # Devrait être (31783, 1, 512)

    def normalize_embeddings(embeddings):
        norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / norm

    # Normaliser les embeddings
    image_embedding = normalize_embeddings(image_embeddings)
    text_embeddings = normalize_embeddings(text_embeddings)

        # Vérifier la forme des embeddings
    print(image_embeddings.shape)  # Devrait être (31783, 1, 512)

    # Créer les indices FAISS
    dimension = image_embeddings.shape[2]  # La dimension de chaque embedding (512)
    index_image = faiss.IndexFlatL2(dimension)  # Index pour les images

    # Dictionnaires pour faire le mapping des indices
    faiss_image_mapping = {}  # Mapping index -> vrai nom de fichier image

    # Dossier contenant les images (assurez-vous que les images sont bien dans ce dossier)
    image_folder = '/content/Images'  # Chemin vers le dossier d'images

    # Ajouter les embeddings des images à l'index FAISS
    image_files = os.listdir(image_folder)  # Lister les fichiers dans le dossier images
    for i in range(image_embeddings.shape[0]):
        image_name = image_files[i]  # Utiliser le vrai nom de fichier de l'image
        faiss_image_mapping[i] = image_name  # Mapping entre l'index FAISS et le vrai nom de fichier de l'image
        
        # Supprimer la dimension supplémentaire
        image_embedding = np.squeeze(image_embeddings[i])  # Transforme (1, 512) en (512,)
        
        # Ajouter l'embedding de l'image à l'index FAISS
        print(f"Ajout de l'embedding pour l'image {image_name} avec forme : {image_embedding.shape}")
        index_image.add(np.expand_dims(image_embedding, axis=0).astype('float32'))  # Convertir en 2D (1, 512) pour FAISS

    # Dimensions des embeddings
    dimension = image_embeddings.shape[2]  # Dimensions des embeddings (doivent être les mêmes pour images et textes)

    # Créer les indices FAISS
    index_text = faiss.IndexFlatL2(dimension)  # Index pour les textes

    # Dictionnaires pour faire le mapping des indices
    faiss_text_mapping = defaultdict(list)  # Mapping index -> [image_name_0, image_name_1, ...]

    # Dossier contenant les images (assurez-vous que les images sont bien dans ce dossier)
    image_folder = '/content/Images'  # Chemin vers le dossier d'images

    count = 0
    # Ajouter les embeddings des textes à l'index FAISS
    for i in range(text_embeddings.shape[0]):
        # Récupérer le nom de l'image associé au texte
        image_name = f"{image_files[i//5]}_{count}"

        # Créer l'identifiant du texte sous la forme 'image_name_(i)'
        faiss_text_mapping[i].append(image_name)  # Mapping entre index texte et image

        # S'assurer que l'embedding a la bonne forme
        text_embedding = np.squeeze(text_embeddings[i])  # Transforme (1, 512) en (512,)
        text_embedding = np.expand_dims(text_embedding, axis=0)  # Ajouter la dimension pour obtenir (1, 512)

        # Ajouter l'embedding du texte à l'index FAISS
        index_text.add(text_embedding.astype('float32'))  # Ajouter l'embedding du texte
        print(f"Ajout de l'embedding pour le texte {image_name} avec forme : {text_embedding.shape}")
        count += 1
        if count == 5:
            count = 0

    print("Index d'images et de textes créés avec succès.")
