import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from Projet_recherche import Ui_MainWindowRecherche as Ui_Interface1 # Importer la première interface
from Projet_indexation import Ui_MainWindowIndexation as Ui_Interface2  # Importer la deuxième interface

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fenêtre principale avec plusieurs widgets")
        self.setGeometry(100, 100, 1200, 800)

        # Création des deux widgets
        self.widget1 = Ui_Interface1()
        self.widget2 = Ui_Interface2()

        # Layout pour afficher les widgets
        self.layout = QtWidgets.QVBoxLayout(self)

        # Ajouter les widgets à la fenêtre principale
        self.layout.addWidget(self.widget1)
        self.layout.addWidget(self.widget2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Création de la fenêtre principale (si tu veux combiner les deux interfaces)
    main_window = MainWindow()
    
    # Tu peux afficher l'interface de recherche ou d'indexation selon tes besoins
    ui_recherche = Ui_Interface1()
    ui_recherche.setupUi(main_window)  # Ajoute l'interface de recherche dans la fenêtre principale
    
    # Si tu veux, tu peux aussi créer une instance de l'interface d'indexation
    # ui_indexation = Ui_IndexationWindow()
    # ui_indexation.setupUi(main_window)
    
    main_window.show()
    
    sys.exit(app.exec_())  # Exécute l'application Qt