# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TP3_recherche.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import os 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QFileDialog 
import cv2 
import numpy as np 
from skimage.transform import resize 
from skimage.io import imread 
from skimage.feature import hog 
from skimage import exposure 
from matplotlib import pyplot as plt 
from functions_recherche import extractReqFeatures, showDialog, generateSIFT, generateHistogramme_HSV, generateHistogramme_Color, generateORB 
from distances import * 
filenames= "MIR_DATASETS_B" 
folder_model="MIR_DATASETS_B" 
import functions_recherche
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import torch
import torchvision.transforms as transforms
import pickle
from PIL import Image
import json
from scipy.spatial.distance import cosine
from PyQt5.QtWidgets import QMessageBox



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 800)
        
        # Créer un widget central qui sera ajouté à la QScrollArea
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 10, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.Panel)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.checkBox_HistC = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_HistC.setGeometry(QtCore.QRect(210, 50, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_HistC.setFont(font)
        self.checkBox_HistC.setObjectName("checkBox_HistC")
        self.checkBox_HSV = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_HSV.setGeometry(QtCore.QRect(290, 50, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_HSV.setFont(font)
        self.checkBox_HSV.setObjectName("checkBox_HSV")
        self.checkBox_SIFT = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_SIFT.setGeometry(QtCore.QRect(210, 80, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_SIFT.setFont(font)
        self.checkBox_SIFT.setObjectName("checkBox_SIFT")
        self.checkBox_ORB = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_ORB.setGeometry(QtCore.QRect(290, 80, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_ORB.setFont(font)
        self.checkBox_ORB.setObjectName("checkBox_ORB")
        self.checkBox_GLCM = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_GLCM.setGeometry(QtCore.QRect(245, 110, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_GLCM.setFont(font)
        self.checkBox_GLCM.setObjectName("checkBox_GLCM")
        self.checkBox_ViT = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_ViT.setGeometry(QtCore.QRect(325, 110, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_ViT.setFont(font)
        self.checkBox_ViT.setObjectName("checkBox_ViT")
        self.checkBox_LBP = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_LBP.setGeometry(QtCore.QRect(360, 80, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_LBP.setFont(font)
        self.checkBox_LBP.setObjectName("checkBox_LBP")
        self.checkBox_HOG = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_HOG.setGeometry(QtCore.QRect(360, 50, 71, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_HOG.setFont(font)
        self.checkBox_HOG.setObjectName("checkBox_HOG")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 250, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_requete = QtWidgets.QLabel(self.centralwidget)
        self.label_requete.setGeometry(QtCore.QRect(10, 290, 431, 251))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_requete.setFont(font)
        self.label_requete.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_requete.setText("")
        self.label_requete.setScaledContents(True)
        self.label_requete.setAlignment(QtCore.Qt.AlignCenter)
        self.label_requete.setObjectName("label_requete")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 700, 1105, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(460, 10, 551, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1020, 10, 300, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        # Create a scroll area to make the gridLayout scrollable
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(460, 290, 551, 251))  # Define size of the scroll area
        self.scrollArea.setWidgetResizable(True)  # This allows the content to resize within the scroll area
        self.scrollArea.setObjectName("scrollArea")
        
        # Create a widget to be placed inside the scroll area
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 551, 251))  # Set the widget size
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        # Create the grid layout and set it to the widget inside the scroll area
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        # Add the widget with the grid layout to the scroll area
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.label_precision = QtWidgets.QLabel(self.centralwidget)
        self.label_precision.setGeometry(QtCore.QRect(1020, 290, 300 , 200))
        self.label_rappel = QtWidgets.QLabel(self.centralwidget)
        self.label_rappel.setGeometry(QtCore.QRect(1020, 491, 300 , 200))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_precision.setFont(font)
        self.label_precision.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_precision.setText("")
        self.label_precision.setScaledContents(True)
        self.label_precision.setAlignment(QtCore.Qt.AlignCenter)
        self.label_precision.setObjectName("label_precision")
        self.label_rappel.setFont(font)
        self.label_rappel.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_rappel.setText("")
        self.label_rappel.setScaledContents(True)
        self.label_rappel.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rappel.setObjectName("label_rappel")

        
        
        
        self.Quitter = QtWidgets.QPushButton(self.centralwidget)
        self.Quitter.setGeometry(QtCore.QRect(1120, 700, 200, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Quitter.setFont(font)
        self.Quitter.setObjectName("Quitter")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(570, 50, 200, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBoxOrbSift = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxOrbSift.setGeometry(QtCore.QRect(775, 50, 200, 41))
        self.comboBoxOrbSift.setObjectName("comboBoxOrbSift")
        self.comboBoxOrbSift.setVisible(False)
        self.comboBoxOrbSift.addItems(["Brute Force", "FLANN"])
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(460, 50, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        
        self.recherche_sur = QtWidgets.QLabel(self.centralwidget)
        self.recherche_sur.setGeometry(QtCore.QRect(460, 100, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recherche_sur.setFont(font)
        self.recherche_sur.setFrameShape(QtWidgets.QFrame.Panel)
        self.recherche_sur.setAlignment(QtCore.Qt.AlignCenter)
        self.recherche_sur.setObjectName("recherche_sur")
        
        self.checkBox_Image = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Image.setGeometry(QtCore.QRect(620, 100, 100, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_Image.setFont(font)
        self.checkBox_Image.setObjectName("checkBox_Image")
        self.checkBox_Text = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Text.setGeometry(QtCore.QRect(705, 100, 70, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_Text.setFont(font)
        self.checkBox_Text.setObjectName("checkBox_Text")
        self.checkBox_CLIP = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_CLIP.setGeometry(QtCore.QRect(790, 100, 70, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_CLIP.setFont(font)
        self.checkBox_CLIP.setObjectName("checkBox_CLIP")
        self.comboBoxCombine = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCombine.setGeometry(QtCore.QRect(705, 200, 100, 41))
        self.comboBoxCombine.setObjectName("comboBoxCombine")
        self.comboBoxCombine.setVisible(True)

        self.comboBoxTop = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxTop.setGeometry(QtCore.QRect(545, 200, 301, 41))
        self.comboBoxTop.setObjectName("comboBoxTop")
        self.top_show = QtWidgets.QLabel(self.centralwidget)
        self.top_show.setGeometry(QtCore.QRect(460, 200, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.top_show.setFont(font)
        self.top_show.setFrameShape(QtWidgets.QFrame.Panel)
        self.top_show.setAlignment(QtCore.Qt.AlignCenter)
        self.top_show.setObjectName("top_show")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(460, 250, 551, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1020, 250, 300, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.chercher = QtWidgets.QPushButton(self.centralwidget)
        self.chercher.setGeometry(QtCore.QRect(910, 200, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.chercher.setFont(font)
        self.chercher.setObjectName("chercher")
        self.calcul_RP = QtWidgets.QPushButton(self.centralwidget)
        self.calcul_RP.setGeometry(QtCore.QRect(1020, 50, 300, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.calcul_RP.setFont(font)
        self.calcul_RP.setObjectName("calcul_RP")


        # Labels des résultats
        self.resultAP = self.create_label(1020, 150, "AP :")
        self.resultAP.setGeometry(QtCore.QRect(1020, 100, 200, 41))
        self.valeur_AP = self.create_label(1230, 100, "")
        self.valeur_AP.setGeometry(QtCore.QRect(1230, 100, 90, 41))

        self.resultMaP = self.create_label(1020, 150, "mAP :")
        self.resultMaP.setGeometry(QtCore.QRect(1020, 150, 200, 41))
        self.valeurMaP = self.create_label(1230, 150, "")
        self.valeurMaP.setGeometry(QtCore.QRect(1230, 150, 90, 41))

        self.resultRP = self.create_label(1020, 200, "R-Precision :")
        self.resultRP.setGeometry(QtCore.QRect(1020, 200, 200, 41))
        self.valeurRP = self.create_label(1230, 200, "")
        self.valeurRP.setGeometry(QtCore.QRect(1230, 200, 90, 41))

        self.charger = QtWidgets.QPushButton(self.centralwidget)
        self.charger.setGeometry(QtCore.QRect(10, 60, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.charger.setFont(font)
        self.charger.setObjectName("charger")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.charger_desc = QtWidgets.QPushButton(self.centralwidget)
        self.charger_desc.setGeometry(QtCore.QRect(230, 140, 190, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.charger_desc.setFont(font)
        self.charger_desc.setObjectName("charger_desc")
        
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setPlaceholderText("Enter search term...")
        self.searchBar.setGeometry(QtCore.QRect(10, 200, 181, 41))

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1203, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.charger.clicked.connect(self.Ouvrir)
        self.searchBar.textChanged.connect(self.on_text_changed)
        self.charger_desc.clicked.connect(self.loadFeatures)
        self.chercher.clicked.connect(self.Recherche)
        self.calcul_RP.clicked.connect(self.calculer_metriques_et_rappel)
        self.Quitter.clicked.connect(self.exit )
         
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Choix de descripteur"))
        self.checkBox_HistC.setText(_translate("MainWindow", "BGR"))
        self.checkBox_HSV.setText(_translate("MainWindow", "HSV"))
        self.checkBox_SIFT.setText(_translate("MainWindow", "SIFT"))
        self.checkBox_ORB.setText(_translate("MainWindow", "ORB"))
        self.checkBox_GLCM.setText(_translate("MainWindow", "GLCM"))
        self.checkBox_ViT.setText(_translate("MainWindow", "ViT"))
        self.checkBox_LBP.setText(_translate("MainWindow", "LBP"))
        self.checkBox_HOG.setText(_translate("MainWindow", "HOG"))        
        self.label_2.setText(_translate("MainWindow", "Image requête"))
        self.label_4.setText(_translate("MainWindow", "Recherche"))
        self.label_5.setText(_translate("MainWindow", "Rappel/Précision"))
        self.Quitter.setText(_translate("MainWindow", "Quitter"))
        self.label_7.setText(_translate("MainWindow", "Distance :"))
        self.recherche_sur.setText(_translate("MainWindow", "Recherche Sur :"))
        self.checkBox_Image.setText(_translate("MainWindow", "Image"))
        self.checkBox_Text.setText(_translate("MainWindow", "Text"))
        self.checkBox_CLIP.setText(_translate("MainWindow", "CLIP"))
        self.top_show.setText(_translate("MainWindow", "Top :"))
        self.label_8.setText(_translate("MainWindow", "Résultats"))
        self.label_9.setText(_translate("MainWindow", "Courbe R et P"))
        self.chercher.setText(_translate("MainWindow", "Recherche"))
        self.calcul_RP.setText(_translate("MainWindow", "Calculer les métriques"))
        self.resultAP.setText(_translate("MainWindow", "Calcul de AP :"))
        self.resultMaP.setText(_translate("MainWindow", "Calcul de MaP :"))
        self.resultRP.setText(_translate("MainWindow", "Calcul de RP :"))
        self.charger.setText(_translate("MainWindow", "Charger Image"))
        self.label_3.setText(_translate("MainWindow", "Requête"))
        self.charger_desc.setText(_translate("MainWindow", "Charger descripteurs"))



    def Ouvrir(self, MainWindow): 
        global fileName 
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "","Image Files (*.png *.jpeg *.jpg *.bmp)") 
        pixmap = QtGui.QPixmap(fileName) 
        pixmap = pixmap.scaled(self.label_requete.width(), 
        self.label_requete.height(), QtCore.Qt.KeepAspectRatio) 
        self.label_requete.setPixmap(pixmap) 
        self.label_requete.setAlignment(QtCore.Qt.AlignCenter)
        self.comboBoxTop.addItems(['Top20','Top50'])
        
    def on_text_changed(self, text):
        # Vérifiez si le texte n'est pas vide
        if text:
            self.comboBoxTop.clear()  # Effacez les éléments précédents
            self.comboBoxTop.addItems(['Top20', 'Top50'])  # Ajoutez les options
        else:
            self.comboBoxTop.clear()  # Si le champ est vide, effacez les éléments
       
        
    def loadFeatures(self, MainWindow):
        folder_models = []
        self.algo_choices = []  # Liste des choix d'algorithmes
        
        if self.checkBox_HistC.isChecked():
            folder_models.append('./BGR')
            self.algo_choices.append(1)
        if self.checkBox_HSV.isChecked():
            folder_models.append('./HSV')
            self.algo_choices.append(2)
        if self.checkBox_SIFT.isChecked():
            folder_models.append('./SIFT')
            self.algo_choices.append(3)
        if self.checkBox_ORB.isChecked():
            folder_models.append('./ORB')
            self.algo_choices.append(4)
        if self.checkBox_GLCM.isChecked():
            folder_models.append('./GLCM')
            self.algo_choices.append(5)
        if self.checkBox_HOG.isChecked():
            folder_models.append('./HOG')
            self.algo_choices.append(6)
        if self.checkBox_LBP.isChecked():
            folder_models.append('./LBP')
            self.algo_choices.append(7)
        if self.checkBox_ViT.isChecked():
            folder_models.append('./ViT')
            self.algo_choices.append(8)

        # Nettoyage du layout
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
    
        # Configuration du comboBox en fonction de l'algorithme choisi
        if filenames:
            # Remise à zéro de la comboBox pour les distances
            self.comboBox.clear()                

            # Vérifier si SIFT ou ORB est sélectionné
            if (len(self.algo_choices) == 1 and (3 in self.algo_choices or 4 in self.algo_choices)) or (len(self.algo_choices) == 2 and (3 in self.algo_choices and 4 in self.algo_choices)):
                self.comboBox.addItems(["Brute force", "Flann"])  # Special options for SIFT and ORB
            else:
                if 3 in self.algo_choices or 4 in self.algo_choices:  # Si SIFT ou ORB sont sélectionnés
                    self.comboBoxOrbSift.setVisible(True)
                else:
                    self.comboBoxOrbSift.setVisible(False)

                # Vérifier si d'autres descripteurs nécessitent d'autres distances
                if any(algo in self.algo_choices for algo in [1, 2, 5, 6, 7, 8]):  # Si d'autres algos sont sélectionnés (par exemple, Histogram, GLCM, LBP...)
                    self.comboBox.addItems(["Euclidienne", "Correlation", "Chi carre", "Intersection", "Bhattacharyya"])  # Default options for other algorithms

        if filenames:
            self.comboBoxTop.addItems(["Top20", "Top50"])
    
        if len(filenames) < 1:
            print("Merci de charger une image avec le bouton Ouvrir")
            return
    
        # Vérifier qu'au moins un descripteur est sélectionné
        if not folder_models:
            print("Merci de sélectionner au moins un descripteur.")
            return
        
        # Chargement des features de chaque descripteur sélectionné
        self.features1 = []  # Liste des features
        pas = 0
        print("Chargement des descripteurs en cours ...")
        
        count = 1 
        total_files_all_folders = sum(1 for folder_model in folder_models for _, _, files in os.walk(folder_model) for file in files if file.endswith(".txt"))

        for folder_model in folder_models:
            if not os.path.exists(folder_model):
                print(f"Erreur : le dossier {folder_model} n'existe pas !")
                return
            for root, _, files in os.walk(folder_model):  # Parcours récursif
                for file in files:
                    if not file.endswith(".txt"):
                        continue
                    
                    feature_path = os.path.join(root, file)
                    feature = np.loadtxt(feature_path)
                    
                    image_name = os.path.basename(file).split('.')[0] + '.jpg'
                    image_path = os.path.join(filenames, image_name)
        
                    self.features1.append((image_path, feature, self.algo_choices[count - 1]))
        
                    pas += 1
                    progress_percentage = (pas / total_files_all_folders) * 100  # Calcul de la progression en pourcentage
                    self.progressBar.setValue(int(progress_percentage))            
            count +=1
        print(f"Chargement terminé : {len(self.features1)} descripteurs chargés.")
    

        
    def Recherche(self, MainWindow):
        if not self.checkBox_Image.isChecked() and not self.checkBox_Text.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez cocher au moins une des options : Image ou Text.")
            msg.exec_()
            return
    
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
    
        self.path_image_plus_proches = []
        self.nom_image_plus_proches = []
        images_deja_ajoutees = set()
    
        if self.comboBoxTop.currentText() == "Top20":
            self.sortie = 20
        elif self.comboBoxTop.currentText() == "Top50":
            self.sortie = 50
        else:
            print("Erreur : Veuillez choisir un Top valide.")
            return
    
        voisins_total = []
        text_results = []
    
        if self.checkBox_Image.isChecked():
            if self.checkBox_CLIP.isChecked():
                model = SentenceTransformer('clip-ViT-B-32')
                model.eval()
                image = Image.open(fileName).convert("RGB")
                query_image_embedding = model.encode([image])[0].reshape(1, -1)
    
                with open("image_embeddings_CLIP.pkl", "rb") as f:
                    image_embeddings = pickle.load(f)
    
                sim_image = {
                    img: cosine_similarity(query_image_embedding, emb.reshape(1, -1))[0][0]
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
    
            else:
                for algo in self.algo_choices:
                    req = extractReqFeatures(fileName, algo)
                    features_par_algo = [f for f in self.features1 if f[2] == algo]
    
                    if not features_par_algo:
                        print(f"Aucun descripteur trouvé pour l'algorithme {algo}.")
                        continue
    
                    if (len(self.algo_choices) == 1 and (algo == 3 or algo == 4)):
                        distanceName = self.comboBox.currentText()
                    else:
                        if algo in [3, 4]:
                            distanceName = self.comboBoxOrbSift.currentText()
                        if algo in [1, 2, 5, 6, 7, 8]:
                            distanceName = self.comboBox.currentText()
    
                    voisins = getkVoisins(features_par_algo, req, self.sortie * 2, distanceName)
    
                    distances = [v[2] for v in voisins]
                    dmin, dmax = min(distances), max(distances)
                    if dmax > dmin:
                        voisins = [(v[0], v[1], (v[2] - dmin) / (dmax - dmin)) for v in voisins]
    
                    for v in voisins:
                        nom = os.path.basename(v[0])
                        if nom not in images_deja_ajoutees:
                            voisins_total.append(v)
                            images_deja_ajoutees.add(nom)
                        if len(voisins_total) >= self.sortie:
                            break
    
                if not voisins_total:
                    print("Aucun voisin trouvé.")
                    return
    
                ordre = True if distanceName in ["Correlation", "Intersection"] else False
                voisins_total.sort(key=lambda x: x[2], reverse=ordre)
                voisins_total = voisins_total[:self.sortie]
    
        if self.checkBox_Text.isChecked():
            query_text = self.searchBar.text().strip()
            if query_text:
                print(f"Recherche pour : {query_text}")
    
                if self.checkBox_CLIP.isChecked():
                    model = SentenceTransformer('clip-ViT-B-32')
                    with open("text_embeddings_CLIP.pkl", "rb") as f:
                        text_embeddings = pickle.load(f)
                    with open("image_embeddings_CLIP.pkl", "rb") as f:
                        image_embeddings = pickle.load(f)
                else:
                    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
                    with open("text_embeddings_LLM.pkl", "rb") as f:
                        text_embeddings = pickle.load(f)
                    with open("image_embeddings_VIT.pkl", "rb") as f:
                        image_embeddings = pickle.load(f)
    
                if not text_embeddings or not image_embeddings:
                    print("⚠ Erreur : Les fichiers d'embeddings sont vides.")
                    return
    
                query_embedding = model.encode(query_text).reshape(1, -1)
    
                similarities = {img: cosine_similarity(query_embedding, emb.reshape(1, -1))[0][0] for img, emb in image_embeddings.items()}
                sorted_results = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    
                for img, sim in sorted_results:
                    nom = os.path.basename(img)
                    if nom not in images_deja_ajoutees:
                        text_results.append((img, sim))
                        images_deja_ajoutees.add(nom)
                    if len(text_results) >= self.sortie:
                        break
    
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Erreur")
                msg.setText("Veuillez entrer un texte de recherche.")
                msg.exec_()
                return
    
        if self.checkBox_Image.isChecked() and self.checkBox_Text.isChecked():
            combined_results = []
            self.comboBoxCombine.clear()
            self.comboBoxCombine.addItems(["Addition", "Multiplication"])
            metric_choice = self.comboBoxCombine.currentText()
    
            if metric_choice == "Addition":
                for img, _, similarity in voisins_total:
                    text_sim = next((sim for sim_img, sim in text_results if sim_img == img), 0)
                    combined_similarity = similarity + text_sim
                    combined_results.append((img, combined_similarity))
            elif metric_choice == "Multiplication":
                for img, similarity in voisins_total:
                    text_sim = next((sim for sim_img, sim in text_results if sim_img == img), 0)
                    combined_similarity = similarity * text_sim
                    combined_results.append((img, combined_similarity))
    
            seen = set()
            final_combined = []
            for img, sim in sorted(combined_results, key=lambda x: x[1], reverse=False):
                nom = os.path.basename(img)
                if nom not in seen:
                    final_combined.append((img, sim))
                    seen.add(nom)
                if len(final_combined) >= self.sortie:
                    break
    
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MIR_DATASETS_B")
            for img, _ in final_combined:
                image_name = os.path.basename(img)
                chemin_parts = image_name.split("_")
                if len(chemin_parts) >= 6:
                    categorie = chemin_parts[4]
                    race = chemin_parts[5]
                    chemin_complet = os.path.join(base_path, categorie, race, image_name)
                elif len(chemin_parts) == 5:
                    categorie = chemin_parts[2]
                    race = chemin_parts[3]
                    chemin_complet = os.path.join(base_path, categorie, race, image_name)
    
                self.path_image_plus_proches.append(chemin_complet)
                self.nom_image_plus_proches.append(img)
    
        elif self.checkBox_Image.isChecked():
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MIR_DATASETS_B")
            for k in range(len(voisins_total)):
                chemin_relatif = voisins_total[k][0]
                image_name = chemin_relatif.split('/')[-1]
                chemin_parts = chemin_relatif.split("_")
                if len(chemin_parts) >= 6:
                    categorie = chemin_parts[4]
                    race = chemin_parts[5]
                    chemin_complet = os.path.join(base_path, categorie, race, image_name)
                elif len(chemin_parts) == 5:
                    categorie = chemin_parts[2]
                    race = chemin_parts[3]
                    chemin_complet = os.path.join(base_path, categorie, race, image_name)
                else:
                    continue
    
                self.path_image_plus_proches.append(chemin_complet)
                self.nom_image_plus_proches.append(image_name)
    
        elif self.checkBox_Text.isChecked():
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MIR_DATASETS_B")
            for img, _ in text_results:
                image_name = os.path.basename(img)
                chemin_parts = image_name.split("_")
                if len(chemin_parts) == 5:
                    categorie = chemin_parts[2]
                    race = chemin_parts[3]
                    img = os.path.join(base_path, categorie, race, image_name)
                self.path_image_plus_proches.append(img)
                self.nom_image_plus_proches.append(img)
    
        # Affichage
        col = 3
        k = 0
        for i in range(math.ceil(len(self.path_image_plus_proches) / col)):
            for j in range(col):
                if k >= len(self.path_image_plus_proches):
                    break
    
                chemin_image = self.path_image_plus_proches[k]
                if not os.path.exists(chemin_image):
                    k += 1
                    continue
    
                img = cv2.imread(chemin_image, cv2.IMREAD_COLOR)
                if img is None:
                    k += 1
                    continue
    
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                bytesPerLine = 3 * w
                qImg = QtGui.QImage(img.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
    
                label = QtWidgets.QLabel("")
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setPixmap(pixmap.scaled(min(int(0.3 * w), 150), min(150, int(0.3 * h)),
                                              QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
                self.gridLayout.addWidget(label, i, j)
                k += 1


    def rappel_precision(self): 
        nb_images_pertinentes = 0
        nb_images_pertinentes_recuperees = 0
        liste_nb_images_pertinentes_recuperees = []
        rappels = [] 
        precisions = [] 
        
        # Race de l'image requête
        filename_req = os.path.basename(fileName)
        try:
            classe_image_requete = filename_req.split("_")[3]
            match = filename_req.split("_")[4]
        except IndexError:
            print(f"Erreur : Impossible d'extraire une classe depuis le nom {filename_req}")
            return
        
        # Calcul du nombre d'images pertinentes
        dossier_racine = "MIR_DATASETS_B"
        for dossier_principal in os.listdir(dossier_racine):
            chemin_dossier_principal = os.path.join(dossier_racine, dossier_principal)
            if os.path.isdir(chemin_dossier_principal):
                for dossier_race in os.listdir(chemin_dossier_principal):
                    if dossier_race == classe_image_requete:
                        chemin_dossier_race = os.path.join(chemin_dossier_principal, dossier_race)
                        nb_images_pertinentes = len([
                            f for f in os.listdir(chemin_dossier_race)
                            if os.path.isfile(os.path.join(chemin_dossier_race, f))
                        ])
                        break
        
        if nb_images_pertinentes == 0:
            print(f"Aucune image trouvée pour la classe {classe_image_requete}")
            return
        print(f'nb_images_pertinentes : {nb_images_pertinentes}')
        
        # Calcul du nombre d'images pertinentes récupérées
        for i in range(self.sortie):
            print(f'____________image {i+1}____________')
            nom_proche = self.nom_image_plus_proches[i]
            try:
                classe_image_proche = nom_proche.split("_")[3]
            except IndexError:
                print(f"Erreur : Impossible d'extraire une classe depuis le nom {nom_proche}")
                liste_nb_images_pertinentes_recuperees.append(0)
                continue
        
            if classe_image_requete == classe_image_proche:
                liste_nb_images_pertinentes_recuperees.append(1)
                nb_images_pertinentes_recuperees += 1
                print('Bonne classe!')
            else:
                liste_nb_images_pertinentes_recuperees.append(0)
                print(f'nb_images_pertinentes_recuperees : {nb_images_pertinentes_recuperees}')
            
            precision = nb_images_pertinentes_recuperees / (i + 1)
            rappel = nb_images_pertinentes_recuperees / nb_images_pertinentes
            print(f'Rappel : {rappel}')
            print(f'Precision : {precision}')
            rappels.append(rappel)
            precisions.append(precision)
        
        # Sauvegarde des courbes
        save_folder = os.path.join(".", match)
        if not os.path.exists(save_folder): 
            os.makedirs(save_folder) 
        
        save_precision = os.path.join(save_folder, f'{match}_precision.png')
        save_rappel = os.path.join(save_folder, f'{match}_rappel.png')
    
        # Courbe Précision
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(precisions)+1), precisions, marker='o', color='blue')
        plt.xlabel("Nombre d'images récupérées")
        plt.ylabel("Précision")
        plt.title(f"Courbe de Précision - Image {match}")
        plt.grid(True)
        plt.savefig(save_precision, format='png', dpi=600)
        plt.close()
    
        # Courbe Rappel
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(rappels)+1), rappels, marker='o', color='green')
        plt.xlabel("Nombre d'images récupérées")
        plt.ylabel("Rappel")
        plt.title(f"Courbe de Rappel - Image {match}")
        plt.grid(True)
        plt.savefig(save_rappel, format='png', dpi=600)
        plt.close()
    
        # Affichage dans Qt
        # Précision
        img_prec = cv2.imread(save_precision, 1)
        b, g, r = cv2.split(img_prec)
        img_prec = cv2.merge([r, g, b])
    
        label_prec_width = self.label_precision.width()
        label_prec_height = self.label_precision.height()
        resized_prec = cv2.resize(img_prec, (label_prec_width, label_prec_height), interpolation=cv2.INTER_AREA)
    
        qImg_prec = QtGui.QImage(resized_prec.data, label_prec_width, label_prec_height, 3 * label_prec_width, QtGui.QImage.Format_RGB888)
        pixmap_prec = QtGui.QPixmap.fromImage(qImg_prec)
        self.label_precision.setAlignment(QtCore.Qt.AlignCenter)
        self.label_precision.setPixmap(pixmap_prec)
    
        # Rappel
        img_rapp = cv2.imread(save_rappel, 1)
        b, g, r = cv2.split(img_rapp)
        img_rapp = cv2.merge([r, g, b])
    
        label_rapp_width = self.label_rappel.width()
        label_rapp_height = self.label_rappel.height()
        resized_rapp = cv2.resize(img_rapp, (label_rapp_width, label_rapp_height), interpolation=cv2.INTER_AREA)
    
        qImg_rapp = QtGui.QImage(resized_rapp.data, label_rapp_width, label_rapp_height, 3 * label_rapp_width, QtGui.QImage.Format_RGB888)
        pixmap_rapp = QtGui.QPixmap.fromImage(qImg_rapp)
        self.label_rappel.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rappel.setPixmap(pixmap_rapp)
    
        return rappels, precisions, liste_nb_images_pertinentes_recuperees


    
    def create_label(self, x, y, text):
        """Crée un QLabel avec du style."""
        label = QtWidgets.QLabel(text, self.centralwidget)
        label.setGeometry(QtCore.QRect(x, y, 250, 41))
        font = QtGui.QFont("Calibri", 11, QtGui.QFont.Bold)
        label.setFont(font)
        label.setFrameShape(QtWidgets.QFrame.Panel)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label
    def average_precision(self, rappels, precisions):
        """Calcul de l'Average Precision (AP) : moyenne des précisions aux points où un rappel augmente."""
        ap = 0.0
        prev_recall = 0.0
    
        for recall, precision in zip(rappels, precisions):
            delta_recall = recall - prev_recall
            ap += precision * delta_recall
            prev_recall = recall
    
        return ap

    def mean_average_precision(self, liste_AP):
        if not liste_AP:
            return 0.0
        return sum(liste_AP) / len(liste_AP)

    
    def r_precision(self, liste_pertinentes_recuperees, R):
        top_R = liste_pertinentes_recuperees[:R]  # Prendre les R premiers résultats
        nb_pertinents_dans_top_R = sum(top_R)
        
        r_precision_value = nb_pertinents_dans_top_R / R
        return r_precision_value


    def calculer_metriques(self):
        """Calcul des métriques à partir des vraies données et affichage des résultats."""
    
        # Appeler la fonction rappel_precision() pour obtenir les valeurs de rappel et précision
        rappels, precisions, liste_nb_images_pertinentes_recuperees = self.rappel_precision()  # récupérer les résultats de rappel et précision
        # Calculer les métriques
        ap = self.average_precision(rappels, precisions)  # Calculer l'Average Precision
        map_value = self.mean_average_precision([ap])  # Calculer la Mean Average Precision (mAP)
        if self.comboBoxTop.currentText() == "Top20":
            R = 20
        if self.comboBoxTop.currentText() == "Top50":
            R = 50 
        rp = self.r_precision(liste_nb_images_pertinentes_recuperees, R)  # Calculer la R-Precision
        
        # Afficher les résultats dans les labels
        self.valeur_AP.setText(f"{ap:.4f}")
        self.valeurMaP.setText(f"{map_value:.4f}")
        self.valeurRP.setText(f"{rp:.4f}")
        
    def calculer_metriques_et_rappel(self):
        """Appelle les fonctions rappel_precision et calculer_metriques."""
        # Appeler la fonction rappel_precision pour calculer les valeurs
        rappels, precisions, liste_nb_images_pertinentes_recuperees = self.rappel_precision()  # Cette ligne doit renvoyer les bonnes données
        
        # Vérifier si les rappels et précisions ne sont pas vides avant de continuer
        if not rappels or not precisions or not liste_nb_images_pertinentes_recuperees:
            print("Erreur dans le calcul des rappels ou précisions.")
            return
        
        # Appeler la fonction calculer_metriques pour afficher les résultats dans les labels
        self.calculer_metriques()  # Cela calcule et affiche les métriques (AP, mAP, R-Precision)


    # def loadFeaturesText(self):
    #     query_text = self.searchBar.text().strip()  # Récupérer et nettoyer la requête
    #     self.comboBoxTop.addItems(['Top20','Top50'])
    #     if query_text:
    #         print(f"🔍 Recherche pour : {query_text}")
            
    #         # Vérifier le choix Top 20 ou Top 50
    #         if self.comboBoxTop.currentText() == "Top20":
    #             self.sortie = 20
    #         elif self.comboBoxTop.currentText() == "Top50":
    #             self.sortie = 50
    #         else:
    #             self.sortie = 5  # Valeur par défaut
    
    #         self.perform_search(query_text)  # Lancer la recherche
    #     else:
    #         print("⚠ Aucun texte saisi dans la barre de recherche.")
    
    # def perform_search(self, query):
    #    try:
    #        # 🔹 Récupérer le nombre d’images à afficher (Top 20 ou Top 50)
    #        if self.comboBoxTop.currentText() == "Top20":
    #            self.sortie = 20
    #        elif self.comboBoxTop.currentText() == "Top50":
    #            self.sortie = 50
    #        else:
    #            self.sortie = 5  # Valeur par défaut si rien n'est sélectionné
       
    #        # Charger le modèle pour l'encodage du texte
    #        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
       
    #        # Charger les embeddings textuels et d'images
    #        with open("text_embeddings.pkl", "rb") as f:
    #            text_embeddings = pickle.load(f)
       
    #        with open("image_embeddings.pkl", "rb") as f:
    #            image_embeddings = pickle.load(f)
       
    #        if not text_embeddings or not image_embeddings:
    #            print("⚠ Erreur : Les fichiers d'embeddings sont vides.")
    #            return
       
    #        # 🔹 Encodage de la requête utilisateur
    #        query_embedding = model.encode(query).reshape(1, -1)
       
    #        # 🔹 Calcul des similarités entre la requête et chaque image
    #        similarities = {img: cosine_similarity(query_embedding, emb.reshape(1, -1))[0][0] for img, emb in image_embeddings.items()}
       
    #        # 🔹 Trier les images par score de similarité décroissant
    #        sorted_results = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
       
    #        # 🔹 Sélectionner seulement le Top choisi (20 ou 50)
    #        sorted_results = sorted_results[:self.sortie]
       
    #        # 🔹 Afficher les résultats dans la console
    #        print(f"\n✅ Top {self.sortie} résultats :")
    #        for img, similarity in sorted_results:
    #            print(f"🖼 {img}: Similarité = {similarity:.4f}")
       
    #        # 🔹 Afficher les images trouvées dans l'interface
    #        self.display_images([img for img, _ in sorted_results])
       
    #    except FileNotFoundError:
    #        print("❌ Erreur : Un fichier d'embeddings est introuvable.")
    #    except Exception as e:
    #        print(f"❌ Une erreur est survenue : {e}")

    
    # def display_images(self, image_paths):
    #     """
    #     Affiche les images trouvées dans l'interface utilisateur.
    #     """
    #     # Limiter l'affichage aux `self.sortie` images
    #     image_paths = image_paths[:self.sortie]
    
    #     # Remise à zéro de la grille
    #     for i in reversed(range(self.gridLayout.count())):
    #         self.gridLayout.itemAt(i).widget().setParent(None)
    
    #     col = 3  # Nombre de colonnes d'affichage
    #     k = 0  # Compteur
    
    #     # Définir la taille maximale de l'image
    #     max_image_width = 150
    #     max_image_height = 150
    
    #     # Chemin de base du dataset
    #     base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MIR_DATASETS_B")
    
    #     for i in range(math.ceil(len(image_paths) / col)):
    #         for j in range(col):
    #             if k >= len(image_paths):
    #                 break
    
    #             chemin_image = image_paths[k]
    
    #             # Extraire catégorie et race
    #             chemin_parts = chemin_image.split('_')
    
    #             if len(chemin_parts) >= 4:
    #                 categorie, race = chemin_parts[2], chemin_parts[3]
    #             else:
    #                 print(f"⚠ Erreur : Format de nom invalide pour {chemin_image}")
    #                 k += 1
    #                 continue
    
    #             # Construire le chemin complet
    #             chemin_complet = os.path.join(base_path, categorie, race, chemin_image)
    
    #             if not os.path.exists(chemin_complet):
    #                 print(f"❌ Erreur : L'image {chemin_complet} n'existe pas.")
    #                 k += 1
    #                 continue
    
    #             # Charger l'image
    #             img = cv2.imread(chemin_complet, cv2.IMREAD_COLOR)
    #             if img is None:
    #                 print(f"❌ Erreur : Impossible de charger {chemin_complet}.")
    #                 k += 1
    #                 continue
    
    #             # Convertir en RGB
    #             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    #             # Convertir en QImage
    #             height, width, channel = img.shape
    #             bytesPerLine = 3 * width
    #             qImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    #             pixmap = QtGui.QPixmap.fromImage(qImg)
    
    #             # Créer un label pour l'image
    #             label = QtWidgets.QLabel("")
    #             label.setAlignment(QtCore.Qt.AlignCenter)
    #             label.setPixmap(pixmap.scaled(min(int(0.3 * width), max_image_width),
    #                                           min(int(0.3 * height), max_image_height),
    #                                           QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
    
    #             # Ajouter l'image à la grille
    #             self.gridLayout.addWidget(label, i, j)
    
    #             k += 1




        
    def exit(self, MainWindow):
            sys.exit()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
