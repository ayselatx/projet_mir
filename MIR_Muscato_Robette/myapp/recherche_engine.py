import pickle
import os
from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Rechercheur:
    def __init__(self):
        # Chemin vers le dossier "media/MIR_DATASETS_B"
        self.base_path = os.path.join(
            os.getcwd(), "myapp"
        )
        self.sortie = 10

    def lancer_recherche(self, image_name=None, texte=None):
        results = []

        if image_name:
            results += self.recherche_image(image_name)

        if texte:
            results += self.recherche_texte(texte)

        return results[:self.sortie]

    def recherche_image(self, image_name):
        print(f'ImageName : {image_name}')
        current_directory = os.getcwd()
        print("Le dossier actuel est :", current_directory)

        # Supprimer le "/media" du début du nom de l'image
        path = os.path.join(self.base_path, image_name.lstrip("/"))
        print(f'Chemin de l\'image : {path}')

        try:
            image = Image.open(path).convert("RGB")
        except FileNotFoundError:
            print(f"Erreur : L'image à {path} n'a pas été trouvée.")
            return []

        model = SentenceTransformer('clip-ViT-B-32')
        query_embedding = model.encode([image])[0].reshape(1, -1)

        path_embedding_image = os.path.join(self.base_path,"media" ,"image_embeddings_CLIP.pkl")

        with open(path_embedding_image, "rb") as f:
            image_embeddings = pickle.load(f)

        sim_scores = {
            img: cosine_similarity(query_embedding, emb.reshape(1, -1))[0][0]
            for img, emb in image_embeddings.items()
        }

        sorted_images = sorted(sim_scores.items(), key=lambda x: x[1], reverse=True)
        return [os.path.join(current_directory,"media","MIR_DATASETS_B", img) for img, _ in sorted_images[:self.sortie]]

    def recherche_texte(self, texte):
        model = SentenceTransformer('clip-ViT-B-32')
        query_embedding = model.encode(texte).reshape(1, -1)

        path_embedding_text = os.path.join(self.base_path, "text_embeddings_CLIP.pkl")

        with open(path_embedding_text, "rb") as f:
            text_embeddings = pickle.load(f)

        sim_scores = {
            img: cosine_similarity(query_embedding, emb.reshape(1, -1))[0][0]
            for img, emb in text_embeddings.items()
        }

        sorted_images = sorted(sim_scores.items(), key=lambda x: x[1], reverse=True)
        return [os.path.join("static", img) for img, _ in sorted_images[:self.sortie]]
