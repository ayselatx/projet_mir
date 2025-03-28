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
    if not os.path.isdir("SIFT"):
        os.mkdir("SIFT")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        featureSum = 0
        sift = cv2.SIFT_create()  
        kps , des = sift.detectAndCompute(img,None)

        num_image, _ = path.split(".")
        np.savetxt("SIFT/"+str(num_image)+".txt" ,des)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        
        featureSum += len(kps)
        i+=1
    print(f"Indexation SIFT terminÃ©e en {time.time() - start} secondes !!!!")  
    


def generateORB(filenames, progressBar):
    start = time.time()
    
    # Créer le répertoire ORB s'il n'existe pas déjà
    if not os.path.isdir("ORB"):
        os.mkdir("ORB")
    
    i = 0
    # Parcourir tous les fichiers dans le répertoire donné
    for root, dirs, files in os.walk(filenames):
        for file in files:
            # Vérifier si le fichier est une image avec l'extension .jpg, .jpeg ou .png
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(root, file)  # Chemin complet de l'image
                
                # Lire l'image
                img = cv2.imread(img_path)
                
                # Créer un objet ORB pour extraire les descripteurs
                orb = cv2.ORB_create()
                key_points, descriptors = orb.detectAndCompute(img, None)
                
                # Extraire le nom de l'image sans extension
                num_image = os.path.splitext(file)[0]
                
                # Sauvegarder les descripteurs dans un fichier texte
                np.savetxt(f"ORB/{num_image}.txt", descriptors)
                
                # Mettre à jour la barre de progression
                i += 1
                progressBar.setValue(100 * (i / len(files)))
    
    print(f"Indexation ORB terminee en {time.time() - start} secondes !!!!")
    
def generateGLCM(filenames, progressBar): 
    start = time.time()
    if not os.path.isdir("GLCM"): 
        os.mkdir("GLCM") 
    distances=[1,-1] 
    angles=[0, np.pi/4, np.pi/2, 3*np.pi/4] 
    i=0 
    for path in os.listdir(filenames): 
        image = cv2.imread(filenames+"/"+path) 
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
        gray = img_as_ubyte(gray) 
        glcmMatrix = greycomatrix(gray, distances=distances, angles=angles, normed=True) 
        glcmProperties1 = greycoprops(glcmMatrix,'contrast').ravel() 
        glcmProperties2 = greycoprops(glcmMatrix,'dissimilarity').ravel() 
        glcmProperties3 = greycoprops(glcmMatrix,'homogeneity').ravel() 
        glcmProperties4 = greycoprops(glcmMatrix,'energy').ravel() 
        glcmProperties5 = greycoprops(glcmMatrix,'correlation').ravel() 
        glcmProperties6 = greycoprops(glcmMatrix,'ASM').ravel() 
        feature = np.array([glcmProperties1,glcmProperties2,glcmProperties3,glcmProperties4,glcmProperties5, glcmProperties6]).ravel() 
        num_image, _ = path.split(".") 
        np.savetxt("GLCM/"+str(num_image)+".txt" ,feature) 
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames)))) 
        i+=1 
    print("indexation GLCM termine en {time.time() - start} secondes!!!!") 
    
def generateLBP(filenames, progressBar): 
    start = time.time()
    if not os.path.isdir("LBP"): 
        os.mkdir("LBP") 
    i=0 
    for path in os.listdir(filenames): 
        img = cv2.imread(filenames+"/"+path) 
        points=8 
        radius=1 
        method='default' 
        subSize=(70,70) 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        img = cv2.resize(img,(350,350)) 
        fullLBPmatrix = local_binary_pattern(img,points,radius,method) 
        histograms = [] 
        for k in range(int(fullLBPmatrix.shape[0]/subSize[0])): 
            for j in range(int(fullLBPmatrix.shape[1]/subSize[1])): 
                subVector = fullLBPmatrix[k*subSize[0]:(k+1)*subSize[0],j*subSize[1]:(j+1)*subSize[1]].ravel() 
                subHist,edges = np.histogram(subVector,bins=int(2**points),range=(0,2**points)) 
                histograms = np.concatenate((histograms,subHist),axis=None) 
        num_image, _ = path.split(".") 
        np.savetxt("LBP/"+str(num_image)+".txt" ,histograms) 
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))    
        i+=1 
    print("indexation LBP termine en {time.time() - start} secondes!!!!") 
