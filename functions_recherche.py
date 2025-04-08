from PyQt5.QtWidgets import  QMessageBox
import cv2
import numpy as np
from skimage import img_as_ubyte
import torch 
import os
import torchvision.transforms as transforms 
from sentence_transformers import SentenceTransformer
import torchvision.models as models 
from PIL import Image 
from skimage.feature import greycomatrix, greycoprops, local_binary_pattern
import faiss
import pickle
from tqdm import tqdm

# def affiche_top(comboBoxTop, fileName):
#     # Nettoyer la comboBox et ajouter seulement les options valides
#     comboBoxTop.clear()
    
#     if fileName == '':
#             comboBoxTop.addItem("Top20")
#             comboBoxTop.addItem("Top50")
#             comboBoxTop.addItem("Top100")
#     else : 
#         filename_req = os.path.basename(fileName)
#         try:
#             classe_image_requete = filename_req.split("_")[3]
#         except IndexError:
#             print(f"Erreur : Impossible d'extraire une classe depuis le nom {filename_req}")
#             return None
    
#         # Chercher le nombre d'images pertinentes
#         dossier_racine = "MIR_DATASETS_B"
#         nb_images_pertinentes = 0
    
#         for dossier_principal in os.listdir(dossier_racine):
#             chemin_dossier_principal = os.path.join(dossier_racine, dossier_principal)
#             if os.path.isdir(chemin_dossier_principal):
#                 for dossier_race in os.listdir(chemin_dossier_principal):
#                     if dossier_race == classe_image_requete:
#                         chemin_dossier_race = os.path.join(chemin_dossier_principal, dossier_race)
#                         nb_images_pertinentes = len([
#                             f for f in os.listdir(chemin_dossier_race)
#                             if os.path.isfile(os.path.join(chemin_dossier_race, f))
#                         ])
#                         break



#         if nb_images_pertinentes >= 20:
#             comboBoxTop.addItem("Top20")
#         if nb_images_pertinentes >= 50:
#             comboBoxTop.addItem("Top50")
#         if nb_images_pertinentes >= 100:
#             comboBoxTop.addItem("Top100")
    
#         # Toujours proposer le max possible
#         comboBoxTop.addItem(f"Top{nb_images_pertinentes}")
#     return int(comboBoxTop.currentText()[3:])



	
def extractReqFeatures(fileName,algo_choice):  
    print(algo_choice)
    if fileName : 
        img = cv2.imread(fileName)
            
        if algo_choice==1: #Couleurs
            histB = cv2.calcHist([img],[0],None,[256],[0,256])
            histG = cv2.calcHist([img],[1],None,[256],[0,256])
            histR = cv2.calcHist([img],[2],None,[256],[0,256])
            vect_features = np.concatenate((histB, np.concatenate((histG,histR),axis=None)),axis=None)
        
        elif algo_choice==2: # Histo HSV
            hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            histH = cv2.calcHist([hsv],[0],None,[180],[0,180])
            histS = cv2.calcHist([hsv],[1],None,[256],[0,256])
            histV = cv2.calcHist([hsv],[2],None,[256],[0,256])
            vect_features = np.concatenate((histH, np.concatenate((histS,histV),axis=None)),axis=None)

        elif algo_choice==3: #SIFT
            sift = cv2.SIFT_create() #cv2.xfeatures2d.SIFT_create() pour py < 3.4 
            # Find the key point
            kps , vect_features = sift.detectAndCompute(img,None)
    
        elif algo_choice==4: #ORB
            orb = cv2.ORB_create()
            # finding key points and descriptors of both images using detectAndCompute() function
            key_point1,vect_features = orb.detectAndCompute(img,None)
            
        elif algo_choice==5: #GLCM
            distances=[1,-1] 
            angles=[0, np.pi/4, np.pi/2, 3*np.pi/4] 
            # finding key points and descriptors of both images using detectAndCompute() function
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
            gray = img_as_ubyte(gray) 
            glcmMatrix = greycomatrix(gray, distances=distances, angles=angles, normed=True) 
            glcmProperties1 = greycoprops(glcmMatrix,'contrast').ravel() 
            glcmProperties2 = greycoprops(glcmMatrix,'dissimilarity').ravel() 
            glcmProperties3 = greycoprops(glcmMatrix,'homogeneity').ravel() 
            glcmProperties4 = greycoprops(glcmMatrix,'energy').ravel() 
            glcmProperties5 = greycoprops(glcmMatrix,'correlation').ravel() 
            glcmProperties6 = greycoprops(glcmMatrix,'ASM').ravel() 
            vect_features = np.array([glcmProperties1,glcmProperties2,glcmProperties3,glcmProperties4,glcmProperties5, glcmProperties6]).ravel()
        elif algo_choice==6: #HOG
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (64,128))
            
            # Resize while maintaining aspect ratio
            #img_resized = resize_and_pad(gray, (64, 128))

            # HOG Descriptor
            win_size = (64, 128)
            block_size = (16, 16)
            block_stride = (8, 8)
            cell_size = (8, 8)
            nbins = 9

            hog_descriptor = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
            vect_features = hog_descriptor.compute(img)

            if vect_features is None or vect_features.shape[0] == 0:
                print("Error: HOG feature extraction failed!")
                return None
            
            vect_features = vect_features.ravel()
        elif algo_choice==7: #LBP
            points=8 
            radius=1 
            method='default' 
            subSize=(70,70) 
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            img = cv2.resize(img,(350,350)) 
            fullLBPmatrix = local_binary_pattern(img,points,radius,method) 
            vect_features = [] 
            for k in range(int(fullLBPmatrix.shape[0]/subSize[0])): 
                for j in range(int(fullLBPmatrix.shape[1]/subSize[1])): 
                    subVector = fullLBPmatrix[k*subSize[0]:(k+1)*subSize[0],j*subSize[1]:(j+1)*subSize[1]].ravel() 
                    subHist,edges = np.histogram(subVector,bins=int(2**points),range=(0,2**points)) 
                    vect_features = np.concatenate((vect_features,subHist),axis=None)
            # finding key points and descriptors of both images using detectAndCompute() function
            print(len(vect_features))
			
        elif algo_choice == 8:  # vit
            model = models.vit_b_16(pretrained=False)
            model.eval()
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            image = Image.open(fileName).convert('RGB')
            image = transform(image).unsqueeze(0)
            with torch.no_grad():
                features = model.features(image)
            vect_features = features.cpu().numpy().flatten()
            
        elif algo_choice == 9:  # clip
            model = SentenceTransformer('clip-ViT-B-32')
            model.eval()
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            image = Image.open(fileName).convert('RGB')
            image = transform(image).unsqueeze(0)
            with torch.no_grad():
                features = model.features(image)
            vect_features = features.cpu().numpy().flatten()

        
        np.savetxt("Methode_"+str(algo_choice)+"_requete.txt" ,vect_features)
        print("saved")
        #print("vect_features", vect_features)
        return vect_features
    
    
def search_by_text(query_text, top_k=5, embeddings_path="embeddings_clip"):
    model = SentenceTransformer('clip-ViT-B-32')
    
    # Chargement de l'index FAISS et des noms d'images
    index_path = os.path.join(embeddings_path, "faiss_image.index")
    names_path = os.path.join(embeddings_path, "image_embeddings_CLIP.pkl")

    if not os.path.exists(index_path) or not os.path.exists(names_path):
        print("⚠️ Index ou embeddings image non trouvés.")
        return []

    index_image = faiss.read_index(index_path)

    with open(names_path, "rb") as f:
        image_embeddings = pickle.load(f)

    img_names = list(image_embeddings.keys())

    # Encodage de la requête texte
    query_emb = model.encode([query_text]).astype('float32')

    # Recherche dans l'index FAISS
    D, I = index_image.search(query_emb, top_k)
    return [(img_names[i], float(D[0][idx])) for idx, i in enumerate(I[0])]


def search_by_image(image, top_k=5, embeddings_path="embeddings_clip"):
    model = SentenceTransformer('clip-ViT-B-32')
    
    # Chargement de l'index FAISS et des textes
    index_path = os.path.join(embeddings_path, "faiss_text.index")
    names_path = os.path.join(embeddings_path, "text_embeddings_CLIP.pkl")

    if not os.path.exists(index_path) or not os.path.exists(names_path):
        print("⚠️ Index ou embeddings texte non trouvés.")
        return []

    index_text = faiss.read_index(index_path)

    with open(names_path, "rb") as f:
        text_embeddings = pickle.load(f)

    text_index_to_img = list(text_embeddings.keys())

    # Encodage de l'image requête
    if isinstance(image, str):  # chemin d'image
        image = Image.open(image).convert("RGB")
    elif isinstance(image, Image.Image):
        pass  # déjà une image PIL
    else:
        raise ValueError("L'entrée image doit être un chemin ou une image PIL.")

    query_emb = model.encode([image]).astype('float32')

    # Recherche dans l'index FAISS
    D, I = index_text.search(query_emb, top_k)
    return [(text_index_to_img[i], float(D[0][idx])) for idx, i in enumerate(I[0])]
