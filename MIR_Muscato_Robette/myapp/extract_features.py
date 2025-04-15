import cv2
import numpy as np
from skimage import img_as_ubyte
import torch 
import os
import torchvision.transforms as transforms 
from sentence_transformers import SentenceTransformer
import torchvision.models as models 
from PIL import Image 
from skimage.feature import local_binary_pattern

#from skimage.feature import greycoprops, local_binary_pattern
import pickle
from tqdm import tqdm
def extractReqFeatures(fileName,algo_choice):  
    if fileName : 
        img = cv2.imread(fileName)
            
        if algo_choice=='BGR': #Couleurs
            histB = cv2.calcHist([img],[0],None,[256],[0,256])
            histG = cv2.calcHist([img],[1],None,[256],[0,256])
            histR = cv2.calcHist([img],[2],None,[256],[0,256])
            vect_features = np.concatenate((histB, np.concatenate((histG,histR),axis=None)),axis=None)
        
        elif algo_choice=='HSV': # Histo HSV
            hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            histH = cv2.calcHist([hsv],[0],None,[180],[0,180])
            histS = cv2.calcHist([hsv],[1],None,[256],[0,256])
            histV = cv2.calcHist([hsv],[2],None,[256],[0,256])
            vect_features = np.concatenate((histH, np.concatenate((histS,histV),axis=None)),axis=None)

        elif algo_choice=='SIFT': #SIFT
            sift = cv2.SIFT_create() #cv2.xfeatures2d.SIFT_create() pour py < 3.4 
            # Find the key point
            kps , vect_features = sift.detectAndCompute(img,None)
    
        elif algo_choice=='ORB': #ORB
            orb = cv2.ORB_create()
            # finding key points and descriptors of both images using detectAndCompute() function
            key_point1,vect_features = orb.detectAndCompute(img,None)
            
        elif algo_choice=='GLCM': #GLCM
            distances=[1,-1] 
            angles=[0, np.pi/4, np.pi/2, 3*np.pi/4] 
            # finding key points and descriptors of both images using detectAndCompute() function
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
            gray = img_as_ubyte(gray) 
            #glcmMatrix = greycomatrix(gray, distances=distances, angles=angles, normed=True) 
            #glcmProperties1 = greycoprops(glcmMatrix,'contrast').ravel() 
            #glcmProperties2 = greycoprops(glcmMatrix,'dissimilarity').ravel() 
            #glcmProperties3 = greycoprops(glcmMatrix,'homogeneity').ravel() 
            #glcmProperties4 = greycoprops(glcmMatrix,'energy').ravel() 
            #glcmProperties5 = greycoprops(glcmMatrix,'correlation').ravel() 
            #glcmProperties6 = greycoprops(glcmMatrix,'ASM').ravel() 
            #vect_features = np.array([glcmProperties1,glcmProperties2,glcmProperties3,glcmProperties4,glcmProperties5, glcmProperties6]).ravel()
        elif algo_choice=='HOG': #HOG
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
        elif algo_choice=='LBP': #LBP
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
			
        elif algo_choice == 'ViT':  # vit
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
            
        elif algo_choice == 'CLIP':  # clip
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
        else :
            print("Algo non reconnu")
            return None

        print("vect_features", vect_features)
        print("vect_features shape", vect_features.shape)
        return vect_features