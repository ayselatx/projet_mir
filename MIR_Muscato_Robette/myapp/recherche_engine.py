import pickle
import os
from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import operator
from .extract_features import extractReqFeatures  # si les deux fichiers sont dans le même module
import faiss
import clip
import torch
from PIL import Image
from collections import defaultdict
import pandas as pd
import torchvision.models as models 





class Rechercheur:
    def __init__(self):
        # Chemin vers le dossier "myapp"
        self.base_path = os.path.join(os.getcwd(), "myapp")
        self.sortie = 20  # Nombre de résultats par défaut

        # Chargement des index Faiss
        self.index_text_faiss = faiss.read_index(os.path.join(self.base_path, "index_text_final.index"))
        self.index_image_faiss = faiss.read_index(os.path.join(self.base_path, "index_image_final.index"))

        # Chargement des mappings entre index Faiss et chemins d'images
        with open(os.path.join(self.base_path, "faiss_image_mapping_final.pkl"), "rb") as f:
            self.faiss_image_mapping = pickle.load(f)

        with open(os.path.join(self.base_path, "faiss_text_mapping_final.pkl"), "rb") as f:
            self.faiss_text_mapping = pickle.load(f)

        # Dictionnaire pour stocker les descriptions d'images
        self.caption_dict = defaultdict(list)
        self.image_descriptions = dict()  # <-- Important : dictionnaire descriptions par image

        media_path = os.path.join(self.base_path, "media")
        csv_path = os.path.join(media_path, "results.csv")

        try:
            # Lecture du fichier CSV contenant les descriptions
            df = pd.read_csv(csv_path, sep='|')
            df.columns = [col.strip() for col in df.columns]  # nettoyage des colonnes

            for _, row in df.iterrows():
                img = row['image_name']
                description = row['comment']
                self.caption_dict[img].append(description)

                # On peut stocker une description simple (par exemple, la première) dans image_descriptions
                if img not in self.image_descriptions:
                    self.image_descriptions[img] = description

        except Exception as e:
            print(f"Erreur lors de la lecture de results.csv ou de la conversion : {e}")


    def lancer_recherche(self, image_name=None, text_query=None, search_type="image", distance="euclidienne", top_results=20, algo_choices=None, combination_type="addition"):
        self.sortie = top_results
        images_deja_ajoutees = set()

        if search_type == "image" and image_name:
            return self.recherche_image(image_name, distance, algo_choices, images_deja_ajoutees)[:self.sortie]

        if search_type == "texte" and text_query:
            return self.recherche_texte(text_query, distance, images_deja_ajoutees)[:self.sortie]

        if search_type == "clip" and (image_name or text_query):
            return self.recherche_clip(query_text=text_query, image_path=image_name, top_k=top_results)

        if "image" in search_type and "texte" in search_type and image_name and text_query:
            voisins_img = self.recherche_image(image_name, distance, algo_choices, set())
            voisins_txt = self.recherche_texte(text_query, distance, set())
            return self.fusionner_scores(voisins_img, voisins_txt, combination_type)[:self.sortie]

        return []


    
    def getkVoisins(self,lfeatures, req, k, distanceName):
        ldistances = [] 
        for i in range(len(lfeatures)): 
            dist = self.calculer_distance(req, lfeatures[i][1], distanceName)  # lfeatures[i][1] = feature
            ldistances.append((lfeatures[i][0], lfeatures[i][1], dist))  # image_path, feature, distance

        # Déterminer l'ordre du tri en fonction de la métrique choisie
        ordre = True if distanceName in ["Correlation", "Intersection"] else False

        # Tri des distances
        ldistances.sort(key=operator.itemgetter(2), reverse=ordre)

        # Retour des k plus proches voisins
        lvoisins = ldistances[:k]
        return lvoisins
    
    def fusionner_scores(self, voisins_img, voisins_txt, combination_type="addition"):
        dict_img = {nom: score for _, nom, score in voisins_img}
        dict_txt = {nom: score for _, nom, score in voisins_txt}

        all_images = set(dict_img.keys()).union(dict_txt.keys())
        fusion = []

        for nom in all_images:
            score_img = dict_img.get(nom, 0.0)
            score_txt = dict_txt.get(nom, 0.0)


            if combination_type == "addition":
                score_final = score_img + score_txt
            elif combination_type == "multiplication":
                score_final = score_img * score_txt
            elif combination_type == "moyenne":
                score_final = (score_img + score_txt) / 2
            else:
                score_final = score_img + score_txt

            chemin_complet = os.path.join(self.base_path, nom)
            fusion.append((chemin_complet, nom, score_final))

        return sorted(fusion, key=lambda x: x[2], reverse=True)




    def recherche_image(self, image_name, distance, algo_choices=None, images_deja_ajoutees=None):
        voisins_total = []
        path = os.path.join(self.base_path, image_name.lstrip("/"))
        algo_choices = algo_choices.split(',')

        try:
            image = Image.open(path).convert("RGB")
        except FileNotFoundError:
            print(f"Erreur : Image {path} introuvable.")
            return []

        if 'clip' in algo_choices:
            model = SentenceTransformer('clip-ViT-B-32')
            query_embedding = model.encode([image])[0].reshape(1, -1)

            with open(os.path.join(self.base_path, "media", "image_embeddings_CLIP.pkl"), "rb") as f:
                image_embeddings = pickle.load(f)

            sim_image = {
                img: cosine_similarity(query_embedding, emb.reshape(1, -1))[0][0]
                for img, emb in image_embeddings.items()
            }

            sorted_img_sim = sorted(sim_image.items(), key=lambda x: x[1], reverse=True)
            for img, score in sorted_img_sim:
                nom = os.path.basename(img)
                if nom not in images_deja_ajoutees:
                    voisins_total.append((img, nom, score))
                    images_deja_ajoutees.add(nom)
                if len(voisins_total) >= self.sortie:
                    break
        elif 'ViT' in algo_choices:
            with open(os.path.join(self.base_path, "media", "image_embeddings_VIT_bis.pkl"), "rb") as f:
                vit_embeddings = pickle.load(f)

            req = extractReqFeatures(path, "ViT")
            sim_image = {
                img: cosine_similarity(req.reshape(1, -1), emb.reshape(1, -1))[0][0]
                for img, emb in vit_embeddings.items()
            }

            sorted_img_sim = sorted(sim_image.items(), key=lambda x: x[1], reverse=True)
            for img, score in sorted_img_sim:
                nom = os.path.basename(img)
                if nom not in images_deja_ajoutees:
                    voisins_total.append((img, nom, score))
                    images_deja_ajoutees.add(nom)
                if len(voisins_total) >= self.sortie:
                    break

        else:
            with open(os.path.join(self.base_path, "features.pkl"), "rb") as f:
                features1 = pickle.load(f)
            for algo in algo_choices:
                algo=str(algo)
                req = extractReqFeatures(path, algo)
                features_par_algo = [(f['image'], f['feature']) for f in features1 if f['algo'] == algo]


                if not features_par_algo:
                    print(f"Aucun descripteur trouvé pour {algo}.")
                    continue

                distanceName = distance
                voisins = self.getkVoisins(features_par_algo, req, self.sortie * 2, distanceName)

                # Normalisation des scores si nécessaire
                distances = [v[2] for v in voisins]
                dmin, dmax = min(distances), max(distances)
                if dmax > dmin:
                    voisins = [(v[0], v[1], (v[2] - dmin) / (dmax - dmin)) for v in voisins]

                for v in voisins:
                    nom = os.path.basename(v[0])
                    if nom not in images_deja_ajoutees:
                        if distanceName == "Correlation" or distanceName == "Intersection":
                            voisins_total.append((v[0], nom, v[2]))
                        else:
                            voisins_total.append((image_name,nom,1-v[2]))
                        images_deja_ajoutees.add(nom)
                    if len(voisins_total) >= self.sortie:
                        break

        return voisins_total
    

    def recherche_texte(self, query_text, distance, images_deja_ajoutees=None):
        voisins_total = []

        if not query_text.strip():
            return []

        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        query_embedding = model.encode(query_text).reshape(1, -1)

        path_text_emb = os.path.join(self.base_path, "media", "text_embeddings_LLM.pkl")
        with open(path_text_emb, "rb") as f:
            text_embeddings = pickle.load(f)

        if not text_embeddings:
            print("Erreur : Embeddings textuels vides.")
            return []

        similarities = {
            img: cosine_similarity(query_embedding, np.array(emb).reshape(1, -1))[0][0]
            for img, emb in text_embeddings.items()
        }

        sorted_results = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        for img, score in sorted_results:
            nom = os.path.basename(img)
            if img not in images_deja_ajoutees:
                voisins_total.append((img, nom, score))
                images_deja_ajoutees.add(nom)
            if len(voisins_total) >= self.sortie:
                break

        return voisins_total
    

    def recherche_clip(self, query_text=None, image_path=None, top_k=20, images_deja_ajoutees=None):
        if images_deja_ajoutees is None:
            images_deja_ajoutees = set()

        voisins_total = []

        if not hasattr(self, "model"):
            self.model, self.preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = clip.tokenize

        if query_text:
            query_text = query_text.lower().strip()
            text_input = self.tokenizer([query_text]).to(self.device)

            with torch.no_grad():
                text_embedding = self.model.encode_text(text_input)
                text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

            D, I = self.index_text_faiss.search(text_embedding.cpu().numpy().astype("float32"), top_k)

            image_scores = defaultdict(list)

            for dist, idx in zip(D[0], I[0]):
                img_path = self.faiss_text_mapping[idx]
                if img_path:
                    score = float(1 - dist)  # Similarity score
                    image_scores[img_path].append(score)

            # Prendre le score max pour chaque image, et s'assurer de ne pas dupliquer les chemins
            for img_path, scores in image_scores.items():
                if img_path not in images_deja_ajoutees:
                    max_score = max(scores)
                    voisins_total.append((img_path, os.path.basename(img_path), max_score))
                    images_deja_ajoutees.add(img_path)
            return sorted(voisins_total, key=lambda x: x[2], reverse=True)


        elif image_path:
            top_k = int(top_k/5)
            image_path_full = os.path.join(self.base_path, image_path.lstrip("/"))

            if not os.path.exists(image_path_full):
                raise FileNotFoundError(f"Image non trouvée : {image_path_full}")

            image_input = self.preprocess(Image.open(image_path_full).convert("RGB")).unsqueeze(0).to(self.device)

            with torch.no_grad():
                image_embedding = self.model.encode_image(image_input)
                image_embedding /= image_embedding.norm(dim=-1, keepdim=True)

            D, I = self.index_image_faiss.search(image_embedding.cpu().numpy().astype("float32"), top_k)

            descriptions_deja_ajoutees = set()
            for dist, idx in zip(D[0], I[0]):
                img_path = self.faiss_image_mapping[idx]
                if img_path:
                    # Récupérer toutes les descriptions associées à l'image
                    descriptions = self.caption_dict.get(img_path, [])
                    for description in descriptions:
                        if description not in descriptions_deja_ajoutees:
                            voisins_total.append((description, description, float(1 - dist)))
                            descriptions_deja_ajoutees.add(description)

            return sorted(voisins_total, key=lambda x: x[2], reverse=True)


        return []













    #____________________Distances_______________
    def euclidean(self, l1, l2):
        return math.dist(l1, l2)

    def chiSquareDistance(self, l1, l2):
        s = 0.0
        for i,j in zip(l1,l2):
            if i == j == 0.0:
                continue
            s += (i - j)**2 / (i + j)
        return s

    def bhatta(self, l1, l2):
        l1 = np.array(l1)
        l2 = np.array(l2)
        num = np.sum(np.sqrt(np.multiply(l1,l2,dtype=np.float64)),dtype=np.float64)
        den = np.sqrt(np.sum(l1,dtype=np.float64)*np.sum(l2,dtype=np.float64))
        return math.sqrt( 1 - num / den )


    def flann(self, a, b):
        # Vérifier si `a` et `b` sont bien des tableaux numpy
        a = np.array(a, dtype=np.float32)
        b = np.array(b, dtype=np.float32)

        #Correction : S'assurer que `a` et `b` sont en 2D
        if a.ndim == 1:
            a = a.reshape(1, -1)  # Convertir en (1, 128) si c'est un vecteur 1D
        if b.ndim == 1:
            b = b.reshape(1, -1)  # Convertir en (1, 128) si c'est un vecteur 1D

        # Vérifier si les descripteurs existent et ont la bonne forme
        if a.ndim != 2 or b.ndim != 2:
            print(f"Erreur : a a {a.shape} dimensions et b a {b.shape} dimensions (attendu 2D)")
            return np.inf

        if a.shape[0] == 0 or b.shape[0] == 0:
            print("Erreur : Un des descripteurs est vide.")
            return np.inf

        if a.shape[1] != b.shape[1]:  
            print(f"Erreur : Les descripteurs ont des dimensions différentes ({a.shape[1]} ≠ {b.shape[1]})")
            return np.inf

        # Utilisation de FLANN pour la recherche des voisins
        flannIndexKDTREE = 1  # Type de recherche (K-D Tree)
        indexParams = dict(algorithm=flannIndexKDTREE, trees=10)
        searchParams = dict(checks=50)  # Nombre d'arbres à interroger
        
        flannMatcher = cv2.FlannBasedMatcher(indexParams, searchParams)
        matches = flannMatcher.match(a, b)  # Recherche des correspondances
        
        # Retourne la distance moyenne des correspondances
        return np.mean([match.distance for match in matches])



    def bruteForceMatching(self, a, b):
        # Vérifier si `a` et `b` sont bien des tableaux numpy
        a = np.array(a, dtype=np.float32)
        b = np.array(b, dtype=np.float32)

        #Correction : S'assurer que `a` et `b` sont en 2D
        if a.ndim == 1:
            a = a.reshape(1, -1)  # Convertir en (1, 128) si c'est un vecteur 1D
        if b.ndim == 1:
            b = b.reshape(1, -1)  # Convertir en (1, 128) si c'est un vecteur 1D

        # Vérifier si les descripteurs existent et ont la bonne forme
        if a.ndim != 2 or b.ndim != 2:
            print(f"Erreur : a a {a.shape} dimensions et b a {b.shape} dimensions (attendu 2D)")
            return np.inf

        if a.shape[0] == 0 or b.shape[0] == 0:
            print("Erreur : Un des descripteurs est vide.")
            return np.inf

        if a.shape[1] != b.shape[1]:  
            print(f"Erreur : Les descripteurs ont des dimensions différentes ({a.shape[1]} ≠ {b.shape[1]})")
            return np.inf

        bf = cv2.BFMatcher(cv2.NORM_L2)  
        matches = bf.match(a, b)  # Trouve les correspondances

        return np.mean([match.distance for match in matches]) if matches else np.inf

    # --- Méthode finale à intégrer dans ta classe Rechercheur :

    def calculer_distance(self, embedding1, embedding2, distance):
        """
        Calcule la distance entre deux embeddings selon le type demandé.
        :param embedding1: premier descripteur
        :param embedding2: second descripteur
        :param distance: nom de la métrique
        :return: valeur de la distance
        """
        embedding1 = np.array(embedding1, dtype=np.float32)
        embedding2 = np.array(embedding2, dtype=np.float32)

        if distance == "cosine":
            return float(cosine_similarity([embedding1], [embedding2])[0][0])

        elif distance == "Euclidienne":
            return self.euclidean(embedding1, embedding2)

        elif distance == "Chi carré":
            return self.chiSquareDistance(embedding1, embedding2)

        elif distance == "Correlation":
            return float(cv2.compareHist(embedding1, embedding2, cv2.HISTCMP_CORREL))

        elif distance == "Intersection":
            return float(cv2.compareHist(embedding1, embedding2, cv2.HISTCMP_INTERSECT))

        elif distance == "Bhattacharyya":
            return self.bhatta(embedding1, embedding2)

        elif distance == "Flann":
            return self.flann(embedding1, embedding2)

        elif distance == "Brute force":
            return self.bruteForceMatching(embedding1, embedding2)

        else:
            raise ValueError(f"Type de distance {distance} non pris en charge.")