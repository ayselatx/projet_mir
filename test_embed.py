import torch
import torchvision.transforms as transforms
from PIL import Image
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Charger le modèle CLIP pour encoder images et textes
model = SentenceTransformer('clip-ViT-B-32')

# Charger le fichier JSON contenant les descriptions textuelles
json_file = "captions.json"
with open(json_file, "r") as f:
    descriptions = json.load(f)

# Générer les embeddings textuels avec CLIP
text_embeddings = {img: model.encode(desc) for img, desc in descriptions.items()}

# Charger et prétraiter l'image
image_path = "C:\\Users\\damoi\\OneDrive - UMONS\\Master1\\Q2\\MIR\\Projet_MIR\\MIR_DATASETS_B\\singes\\gorilla\\4_2_singes_gorilla_3883.jpg"
image = Image.open(image_path).convert("RGB")  # CLIP attend une image PIL ou numpy

# Extraire l'embedding de l'image avec CLIP
image_embedding = model.encode(image)

# Comparer avec les embeddings textuels (similarité cosinus)
similarities = {
    img: 1 - cosine(image_embedding, text_emb)
    for img, text_emb in text_embeddings.items()
}

# Trier par similarité décroissante
sorted_matches = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

# Afficher les résultats
print("Les descriptions les plus proches de l'image sont :")
for i, (img, score) in enumerate(sorted_matches[:15]):  # Top 5
    print(f"{i+1}. {descriptions[img]} (Score: {score:.4f})")
