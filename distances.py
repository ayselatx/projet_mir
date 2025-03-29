import math
import cv2
#from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from skimage import feature
from matplotlib import pyplot as plt
from skimage.feature import hog, greycomatrix, greycoprops, local_binary_pattern
import operator
import collections 
from collections import Counter

def euclidean(l1, l2):
    return math.dist(l1, l2)

def chiSquareDistance(l1, l2):
    s = 0.0
    for i,j in zip(l1,l2):
        if i == j == 0.0:
            continue
        s += (i - j)**2 / (i + j)
    return s

def bhatta(l1, l2):
    l1 = np.array(l1)
    l2 = np.array(l2)
    num = np.sum(np.sqrt(np.multiply(l1,l2,dtype=np.float64)),dtype=np.float64)
    den = np.sqrt(np.sum(l1,dtype=np.float64)*np.sum(l2,dtype=np.float64))
    return math.sqrt( 1 - num / den )


def flann(a, b):
    # Vérification des dimensions
    if a.shape[1] != b.shape[1]:
        print(f"Erreur : Les descripteurs a ({a.shape}) et b ({b.shape}) ont des tailles différentes.")
        return np.inf  # Ou une autre gestion d'erreur appropriée

    # Utilisation de FLANN pour la recherche des voisins
    flannIndexKDTREE = 1  # Type de recherche (K-D Tree)
    indexParams = dict(algorithm=flannIndexKDTREE, trees=10)
    searchParams = dict(checks=50)  # Nombre d'arbres à interroger
    
    flannMatcher = cv2.FlannBasedMatcher(indexParams, searchParams)
    matches = flannMatcher.match(a, b)  # Recherche des correspondances
    
    # Retourne la distance moyenne des correspondances
    return np.mean([match.distance for match in matches])


def bruteForceMatching(a, b):
    a = np.array(a).astype('float32')
    b = np.array(b).astype('float32')
    
    if a.shape[0] == 0 or b.shape[0] == 0:
        return np.inf
    
    # Vérification de la compatibilité des tailles des descripteurs
    if a.shape[0] != b.shape[0]:
        print(f"Erreur : Les descripteurs a ({a.shape}) et b ({b.shape}) ont des tailles différentes.")
        return np.inf
    
    bf = cv2.BFMatcher(cv2.NORM_L2)  # Utilise NORM_L2 pour les descripteurs flottants
    matches = bf.match(a, b)  # Trouve les correspondances
    
    # Retourne la distance moyenne des correspondances
    return np.mean([match.distance for match in matches])



def distance_f(l1,l2,distanceName):
    if distanceName=="Euclidienne":
        distance = euclidean(l1, l2)
    elif distanceName in ["Correlation","Chi carre","Intersection","Bhattacharyya"]:
        if distanceName=="Correlation":
            methode=cv2.HISTCMP_CORREL
            distance = cv2.compareHist(np.float32(l1), np.float32(l2), methode)
        elif distanceName=="Chi carre":
            distance = chiSquareDistance(l1, l2)
        elif distanceName=="Intersection":
            methode=cv2.HISTCMP_INTERSECT
            distance = cv2.compareHist(np.float32(l1), np.float32(l2), methode)
        elif distanceName=="Bhattacharyya":
            distance = bhatta(l1, l2)   
    elif distanceName=="Brute force":
        distance = bruteForceMatching(l1, l2)
    elif distanceName=="Flann":
        distance= flann(l1,l2)
    return distance

def getkVoisins(lfeatures, req, k,distanceName) : 
    ldistances = [] 
    for i in range(len(lfeatures)): 
        dist = distance_f(req, lfeatures[i][1],distanceName)
        ldistances.append((lfeatures[i][0], lfeatures[i][1], dist)) 
    if distanceName in ["Correlation","Intersection"]:
        ordre=True
    else:
        ordre=False
    ldistances.sort(key=operator.itemgetter(2),reverse=ordre) 

    lvoisins = [] 
    for i in range(k): 
        lvoisins.append(ldistances[i]) 
    return lvoisins