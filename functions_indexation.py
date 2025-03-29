#Defintion de toute les fonctions à appeller dans l'interface
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
    msgBox.setText("Merci de sélectionner un descripteur via le menu ci-dessus")
    msgBox.setWindowTitle("Pas de Descripteur sélectionné")
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
    for root, _, files in os.walk(filenames):  # Parcours r�cursif des sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # V�rifier les extensions
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)

                if img is None:
                    print(f"Impossible de lire {img_path}, image ignoree.")
                    continue  # Passer � l'image suivante si erreur        img = cv2.imread(filenames+"/"+path)
                histB = cv2.calcHist([img],[0],None,[256],[0,256])
                histG = cv2.calcHist([img],[1],None,[256],[0,256])
                histR = cv2.calcHist([img],[2],None,[256],[0,256])
                        
                feature = np.hstack((histB.ravel(), histG.ravel(), histR.ravel()))


                num_image = os.path.splitext(file)[0]
                np.savetxt("BGR/"+str(num_image)+".txt" ,feature)
                
                # Mise � jour de la barre de progression
                i += 1
                progressBar.setValue(int(100 * (i / total_images)))
                
    print(f"Indexation Hist Couleur (BGR) terminee en {time.time() - start:.2f} secondes !!!")


def generateHistogramme_HSV(filenames, progressBar):
    import time
    start = time.time()
    
    # Cr�er le dossier s'il n'existe pas
    if not os.path.isdir("HSV"):
        os.mkdir("HSV")

    # Compter le nombre total d'images pour la barre de progression
    total_images = sum(len(files) for _, _, files in os.walk(filenames) if any(f.endswith((".jpg", ".png", ".jpeg")) for f in files))
    if total_images == 0:
        print("Aucune image trouvee !")
        return

    i = 0
    for root, _, files in os.walk(filenames):  # Parcours r�cursif des sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # V�rifier les extensions
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)

                if img is None:
                    print(f"Impossible de lire {img_path}, image ignoree.")
                    continue  # Passer � l'image suivante si erreur

                # Convertir en HSV et calculer les histogrammes
                img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                histH = cv2.calcHist([img_hsv], [0], None, [180], [0, 180])
                histS = cv2.calcHist([img_hsv], [1], None, [256], [0, 256])
                histV = cv2.calcHist([img_hsv], [2], None, [256], [0, 256])

                # Concat�ner les histogrammes
                feature = np.hstack((histH.ravel(), histS.ravel(), histV.ravel()))

                # Sauvegarde dans un fichier
                num_image = os.path.splitext(file)[0]
                np.savetxt(f"HSV/{num_image}.txt", feature)

                # Mise � jour de la barre de progression
                i += 1
                progressBar.setValue(int(100 * (i / total_images)))

    print(f"Indexation Hist HSV terminee en {time.time() - start:.2f} secondes !!!")

def generateHistogramme_HOG(filenames, progressBar):
    start = time.time()
    
    # Cr�er le dossier s'il n'existe pas
    if not os.path.isdir("HOG"):
        os.mkdir("HOG")

    # Compter le nombre total d'images pour la barre de progression
    total_images = sum(1 for _, _, files in os.walk(filenames) for f in files if f.lower().endswith((".jpg", ".jpeg", ".png")))
    
    if total_images == 0:
        print("Aucune image trouve !")
        return

    hog = cv2.HOGDescriptor()  # Cr�ation du descripteur HOG
    i = 0

    for root, _, files in os.walk(filenames):  # Parcours r�cursif des sous-dossiers
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # V�rifier les extensions
                img_path = os.path.join(root, file)
                
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lire en niveaux de gris
                if img is None:
                    print(f"Impossible de lire {img_path}, image ignoree.")
                    continue  # Passer � l'image suivante si erreur
                
                img = cv2.resize(img, (64, 128))  # Redimensionner pour HOG
                feature = hog.compute(img)  # Extraire les caract�ristiques HOG
                
                num_image = os.path.splitext(file)[0]
                np.savetxt(f"HOG/{num_image}.txt", feature)

                progressBar.setValue(int(100 * (i + 1) / total_images))  # Mise � jour correcte
                i += 1
    
    print(f"Indexation HOG terminee en {time.time() - start:.2f} secondes !")   
    
def generateSIFT(filenames, progressBar):
    start = time.time()
    
    # Cr�er le r�pertoire SIFT s'il n'existe pas d�j�
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
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # V�rifie le format de l'image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lit en niveau de gris

                if img is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                sift = cv2.SIFT_create(nfeatures=2000)  # SIFT avec 2000 features max
                key_points, descriptors = sift.detectAndCompute(img, None)

                if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouv�s
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"SIFT/{num_image}.txt", descriptors)
                else:
                    print(f"Aucun descripteur trouve pour {file} donc essaye d'augmente le contrast")
                    # Convertir l'image en niveaux de gris si ce n'est pas d�j� fait
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
                    
                    # Appliquer CLAHE pour am�liorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)
                    key_points, descriptors = sift.detectAndCompute(enhanced_img, None)
                    
                    if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouv�s
                        num_image = os.path.splitext(file)[0]
                        np.savetxt(f"SIFT/{num_image}.txt", descriptors)
                        print(f"ca a fonctionner pour {file}")
                    else:
                        print(f"Aucun descripteur trouve pour {file}")


                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise � jour correcte de la barre de progression

    print(f"Indexation SIFT terminee en {time.time() - start:.2f} secondes !!!!")
    
def generateORB(filenames, progressBar):
    start = time.time()
    
    # Cr�er le r�pertoire SIFT s'il n'existe pas d�j�
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
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # V�rifie le format de l'image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lit en niveau de gris

                if img is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                sift = cv2.ORB_create(nfeatures=2000)  # SIFT avec 2000 features max
                key_points, descriptors = sift.detectAndCompute(img, None)

                if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouv�s
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"ORB/{num_image}.txt", descriptors)
                else:
                    print(f"Aucun descripteur trouve pour {file} donc essaye d'augmente le contrast")
                    # Convertir l'image en niveaux de gris si ce n'est pas d�j� fait
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
                    
                    # Appliquer CLAHE pour am�liorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)
                    key_points, descriptors = sift.detectAndCompute(enhanced_img, None)
                    
                    if descriptors is not None and len(descriptors) > 0:  # Sauvegarde uniquement si descripteurs trouv�s
                        num_image = os.path.splitext(file)[0]
                        np.savetxt(f"ORB/{num_image}.txt", descriptors)
                        print(f"ca a fonctionner pour {file}")
                    else:
                        print(f"Aucun descripteur trouve pour {file}")


                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise � jour correcte de la barre de progression

    print(f"Indexation ORB terminee en {time.time() - start:.2f} secondes !!!!")

    
def generateGLCM(filenames, progressBar): 
    start = time.time()
    
    # Cr�er le dossier GLCM s'il n'existe pas
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
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # V�rifier format image
                img_path = os.path.join(root, file)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Lire en niveaux de gris

                if image is None:
                    print(f"Impossible de lire {img_path}, passage a l'image suivante.")
                    continue

                # Convertir en format appropri� pour GLCM
                gray = img_as_ubyte(image)  

                # Calculer la matrice GLCM
                glcm_matrix = greycomatrix(gray, distances=distances, angles=angles, normed=True)

                # Extraire les propri�t�s GLCM
                features = []
                for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
                    features.extend(greycoprops(glcm_matrix, prop).ravel())

                feature_vector = np.array(features)

                if len(feature_vector) > 0:  # V�rifier que descripteurs trouv�s
                    num_image = os.path.splitext(file)[0]
                    np.savetxt(f"GLCM/{num_image}.txt", feature_vector)
                else:
                    print(f"Aucun descripteur trouve pour {file}, augmentation du contraste...")

                    # Appliquer CLAHE pour am�liorer le contraste localement
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    enhanced_img = clahe.apply(gray)

                    # Recalculer la GLCM avec l'image am�lior�e
                    glcm_matrix = greycomatrix(enhanced_img, distances=distances, angles=angles, normed=True)
                    
                    features = []
                    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
                        features.extend(greycoprops(glcm_matrix, prop).ravel())

                    feature_vector = np.array(features)

                    if len(feature_vector) > 0:  # Sauvegarde si am�lioration r�ussie
                        np.savetxt(f"GLCM/{num_image}.txt", feature_vector)
                        print(f"Amelioration reussie pour {file} !")
                    else:
                        print(f"Echec de l'amelioration pour {file}")

                i += 1
                progressBar.setValue(int(100 * (i / total_images)))  # Mise � jour de la barre de progression

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

    print(f"Indexation LBP terminee en {time.time() - start:.2f} secondes !!!!")

