FROM coolsa/pyqt-designer

# Mise à jour de pip et installation de git
RUN apt-get update && apt-get install -y git

# Mise à jour de pip
RUN python3 -m pip install --upgrade pip

# Installation de toutes les dépendances, y compris Django
RUN pip install \
    django \
    pillow \
    sentence-transformers \
    scikit-learn \
    numpy \
    opencv-python \
    faiss-cpu \
    git+https://github.com/openai/CLIP.git \
    torch \
    pandas \
    torchvision
