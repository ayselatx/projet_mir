import torch
from torch.utils.data import DataLoader  # Ajoutez cet import
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os

class CustomDataset(Dataset):
    def __init__(self, image_folder, transform=None):
        self.image_folder = image_folder
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        # Parcourir tous les sous-dossiers du dossier image_folder
        for root, dirs, files in os.walk(image_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Vérifier les extensions d'image
                    self.image_paths.append(os.path.join(root, file))
                    label = os.path.basename(root)  # Le label est le nom du dossier parent
                    self.labels.append(label)

        # Vérifier que des images ont été trouvées
        if not self.image_paths:
            raise ValueError(f"Aucune image trouvée dans le dossier {image_folder}")
        
        print(f"Classes trouvées : {set(self.labels)}")  # Afficher les classes trouvées pour débogage

    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert("RGB")
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

def train_model_with_custom_images(image_folder, num_epochs=10):
    # Transformations d'images pour VGG16
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Charger les données d'entraînement
    dataset = CustomDataset(image_folder, transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Charger le modèle VGG16 pré-entraîné
    model = models.vgg16(pretrained=True)
    
    # Modifier la dernière couche pour s'adapter au nombre de classes
    num_classes = len(set(dataset.labels))
    model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, num_classes)

    # Définir la fonction de perte et l'optimiseur
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    model.train()  # Mettre le modèle en mode entraînement

    for epoch in range(num_epochs):
        running_loss = 0.0
        for inputs, labels in dataloader:
            optimizer.zero_grad()  # Réinitialiser les gradients
            
            # Passer les images dans le modèle
            outputs = model(inputs)
            
            # Calculer la perte et faire la rétropropagation
            loss = criterion(outputs, labels)
            loss.backward()
            
            optimizer.step()  # Mettre à jour les poids
            
            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss / len(dataloader)}")

    print("Entraînement terminé!")
    return model
