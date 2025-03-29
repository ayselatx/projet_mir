#Defintion de toute les fonctions Ã  appeller dans l'interface
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import os
import cv2
import numpy as np
from skimage.transform import resize
from skimage.feature import hog
from skimage import exposure
from skimage import io, color, img_as_ubyte
from matplotlib import pyplot as plt
from skimage.feature import hog, greycomatrix, greycoprops, local_binary_pattern
import time

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
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        histB = cv2.calcHist([img],[0],None,[256],[0,256])
        histG = cv2.calcHist([img],[1],None,[256],[0,256])
        histR = cv2.calcHist([img],[2],None,[256],[0,256])
        feature = np.concatenate((histB, np.concatenate((histG,histR),axis=None)),axis=None)

        num_image, _ = path.split(".")
        np.savetxt("BGR/"+str(num_image)+".txt" ,feature)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print(f"indexation Hist Couleur terminÃ©e en {time.time() - start} secondes !!!!")

def generateHistogramme_HSV(filenames, progressBar):
    start = time.time()
    if not os.path.isdir("HSV"):
        os.mkdir("HSV")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        histH = cv2.calcHist([img_hsv],[0],None,[180],[0,180])
        histS = cv2.calcHist([img_hsv],[1],None,[256],[0,256])
        histV = cv2.calcHist([img_hsv],[2],None,[256],[0,256])
        feature = np.concatenate((histH, np.concatenate((histS,histV),axis=None)),axis=None)

        num_image, _ = path.split(".")
        np.savetxt("HSV/"+str(num_image)+".txt" ,feature)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print(f"indexation Hist HSV terminÃ©e en {time.time() - start} secondes !!!!")
        
def generateSIFT(filenames, progressBar):
    start = time.time()
    
    # Créer le répertoire SIFT s'il n'existe pas déjà
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
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vérifie le format de l'image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lit en niveau de gris

                if img is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                sift = cv2.SIFT_create(nfeatures=2000)  # SIFT avec 2000 features max
                key_points, descriptors = sift.detectAndCompute(img, None)

                if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouvés
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"SIFT/{num_image}.txt", descriptors)
                else:
                    print(f"Aucun descripteur trouve pour {file} donc essaye d'augmente le contrast")
                    # Convertir l'image en niveaux de gris si ce n'est pas déjà fait
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
                    
                    # Appliquer CLAHE pour améliorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)
                    key_points, descriptors = sift.detectAndCompute(enhanced_img, None)
                    
                    if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouvés
                        num_image = os.path.splitext(file)[0]
                        np.savetxt(f"SIFT/{num_image}.txt", descriptors)
                        print(f"ca a fonctionner pour {file}")
                    else:
                        print(f"Aucun descripteur trouve pour {file}")


                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise à jour correcte de la barre de progression

    print(f"Indexation SIFT terminee en {time.time() - start:.2f} secondes !!!!")

def generateORB(filenames, progressBar):
    start = time.time()
    if not os.path.isdir("ORB"):
        os.mkdir("ORB")
    
    total_images = 0
    for root, dirs, files in os.walk(filenames):
        for file in files:
            if file.endswith((".jpg", ".png", ".jpeg")):
                total_images += 1
    
    i = 0
    for root, dirs, files in os.walk(filenames):
        for file in files:
            if file.endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)
                if img is None:
                    continue  # Si l'image ne peut pas être lue, on passe à la suivante

                orb = cv2.ORB_create(nfeatures=2000, scoreType=cv2.ORB_HARRIS_SCORE, patchSize=31)
                key_points, descrip1 = orb.detectAndCompute(img, None)
                
                if descrip1 is not None and len(descrip1) > 0:  # Vérification que descrip1 n'est pas None et non vide
                    num_image, _ = file.split(".")
                    np.savetxt(f"ORB/{num_image}.txt", descrip1)
                else:
                    print(f"Aucun descripteur trouve pour l'image {file}")
                
                i += 1
                progressBar.setValue(100 * (i / total_images))  # Mise à jour de la barre de progression

    print(f"Indexation ORB terminee en {time.time() - start} secondes!")
    
def generateGLCM(filenames, progressBar): 
    start = time.time()
    
    # Créer le dossier GLCM s'il n'existe pas
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
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vérifier format image
                img_path = os.path.join(root, file)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lire en niveaux de gris

                if image is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                # Convertir en format approprié pour GLCM
                gray = img_as_ubyte(image)  

                # Calculer la matrice GLCM
                glcm_matrix = greycomatrix(gray, distances=distances, angles=angles, normed=True)

                # Extraire les propriétés GLCM
                features = []
                for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
                    features.extend(greycoprops(glcm_matrix, prop).ravel())

                feature_vector = np.array(features)

                if len(feature_vector) > 0:  # Vérifier que descripteurs trouvés
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"GLCM/{num_image}.txt", feature_vector)
                else:
                    print(f"Aucun descripteur trouve pour {file}, augmentation du contraste...")

                    # Appliquer CLAHE pour améliorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)

                    # Recalculer la GLCM avec l'image améliorée
                    glcm_matrix = greycomatrix(enhanced_img, distances=distances, angles=angles, normed=True)
                    
                    features = []
                    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
                        features.extend(greycoprops(glcm_matrix, prop).ravel())

                    feature_vector = np.array(features)

                    if len(feature_vector) > 0:  # Sauvegarde si amélioration réussie
                        np.savetxt(f"GLCM/{num_image}.txt", feature_vector)
                        print(f"Amelioration reussie pour {file} !")
                    else:
                        print(f"Echec de l'amelioration pour {file}")

                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise à jour de la barre de progression

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
                    print(f"Cannot read {img_path}, skipping.")
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
                    print(f"No descriptors found for {file}, applying contrast enhancement.")
                    
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
                        print(f"Fixed {file} with contrast enhancement!")
                    else:
                        print(f"Still no descriptors for {file}")

                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  

    print(f"LBP indexing completed in {time.time() - start:.2f} seconds!")
