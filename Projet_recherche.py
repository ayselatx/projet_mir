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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.checkBox_GLCM.setGeometry(QtCore.QRect(290, 110, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_GLCM.setFont(font)
        self.checkBox_GLCM.setObjectName("checkBox_GLCM")
        self.checkBox_LBP = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_LBP.setGeometry(QtCore.QRect(210, 110, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_LBP.setFont(font)
        self.checkBox_LBP.setObjectName("checkBox_LBP")
        self.checkBox_HOG = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_HOG.setGeometry(QtCore.QRect(380, 50, 71, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_HOG.setFont(font)
        self.checkBox_HOG.setObjectName("checkBox_HOG")
        self.checkBox_Moments = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Moments.setGeometry(QtCore.QRect(380, 80, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_Moments.setFont(font)
        self.checkBox_Moments.setObjectName("checkBox_Moments")
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
        self.progressBar.setGeometry(QtCore.QRect(10, 700, 931, 41))
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
        self.label_5.setGeometry(QtCore.QRect(1020, 10, 251, 31))
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
        self.label_courbe = QtWidgets.QLabel(self.centralwidget)
        self.label_courbe.setGeometry(QtCore.QRect(1020, 290, 251, 251))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_courbe.setFont(font)
        self.label_courbe.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_courbe.setText("")
        self.label_courbe.setScaledContents(True)
        self.label_courbe.setAlignment(QtCore.Qt.AlignCenter)
        self.label_courbe.setObjectName("label_courbe")
        self.Quitter = QtWidgets.QPushButton(self.centralwidget)
        self.Quitter.setGeometry(QtCore.QRect(980, 700, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Quitter.setFont(font)
        self.Quitter.setObjectName("Quitter")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(560, 50, 131, 41))
        self.comboBox.setObjectName("comboBox")
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
        
        self.comboBoxTop = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxTop.setGeometry(QtCore.QRect(765, 50, 131, 41))
        self.comboBoxTop.setObjectName("comboBoxTop")
        self.top_show = QtWidgets.QLabel(self.centralwidget)
        self.top_show.setGeometry(QtCore.QRect(704, 50, 61, 41))
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
        self.label_9.setGeometry(QtCore.QRect(1020, 250, 251, 31))
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
        self.chercher.setGeometry(QtCore.QRect(910, 50, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.chercher.setFont(font)
        self.chercher.setObjectName("chercher")
        self.calcul_RP = QtWidgets.QPushButton(self.centralwidget)
        self.calcul_RP.setGeometry(QtCore.QRect(1020, 50, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.calcul_RP.setFont(font)
        self.calcul_RP.setObjectName("calcul_RP")
        
        self.valeur_AP = QtWidgets.QLabel(self.centralwidget)
        self.valeur_AP.setGeometry(QtCore.QRect(1160, 100, 108, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.valeur_AP.setFont(font)
        self.valeur_AP.setFrameShape(QtWidgets.QFrame.Panel)
        self.valeur_AP.setAlignment(QtCore.Qt.AlignCenter)
        self.valeur_AP.setObjectName("valeur_AP")
        self.resultAP = QtWidgets.QLabel(self.centralwidget)
        self.resultAP.setGeometry(QtCore.QRect(1020, 100, 135, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.resultAP.setFont(font)
        self.resultAP.setFrameShape(QtWidgets.QFrame.Panel)
        self.resultAP.setAlignment(QtCore.Qt.AlignCenter)
        self.resultAP.setObjectName("resultAP")
        
        self.valeurMaP = QtWidgets.QLabel(self.centralwidget)
        self.valeurMaP.setGeometry(QtCore.QRect(1160, 150, 108, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.valeurMaP.setFont(font)
        self.valeurMaP.setFrameShape(QtWidgets.QFrame.Panel)
        self.valeurMaP.setAlignment(QtCore.Qt.AlignCenter)
        self.valeurMaP.setObjectName("valeurMaP")
        self.resultMaP = QtWidgets.QLabel(self.centralwidget)
        self.resultMaP.setGeometry(QtCore.QRect(1020, 150, 135, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.resultMaP.setFont(font)
        self.resultMaP.setFrameShape(QtWidgets.QFrame.Panel)
        self.resultMaP.setAlignment(QtCore.Qt.AlignCenter)
        self.resultMaP.setObjectName("resultMaP")
        
        self.valeurRP = QtWidgets.QLabel(self.centralwidget)
        self.valeurRP.setGeometry(QtCore.QRect(1160, 200, 108, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.valeurRP.setFont(font)
        self.valeurRP.setFrameShape(QtWidgets.QFrame.Panel)
        self.valeurRP.setAlignment(QtCore.Qt.AlignCenter)
        self.valeurRP.setObjectName("valeurRP")
        self.resultRP = QtWidgets.QLabel(self.centralwidget)
        self.resultRP.setGeometry(QtCore.QRect(1020, 200, 135, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.resultRP.setFont(font)
        self.resultRP.setFrameShape(QtWidgets.QFrame.Panel)
        self.resultRP.setAlignment(QtCore.Qt.AlignCenter)
        self.resultRP.setObjectName("resultRP")
        
        self.checkBox_autre = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_autre.setGeometry(QtCore.QRect(380, 110, 81, 17))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_autre.setFont(font)
        self.checkBox_autre.setObjectName("checkBox_autre")
        self.charger = QtWidgets.QPushButton(self.centralwidget)
        self.charger.setGeometry(QtCore.QRect(10, 60, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.charger.setFont(font)
        self.charger.setObjectName("charger")
        self.chargerText = QtWidgets.QPushButton(self.centralwidget)
        self.chargerText.setGeometry(QtCore.QRect(10, 190, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.chargerText.setFont(font)
        self.chargerText.setObjectName("chargerText")
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
        self.charger_desc.setGeometry(QtCore.QRect(230, 140, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.charger_desc.setFont(font)
        self.charger_desc.setObjectName("charger_desc")
        
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(367, 190, 70, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.search.setFont(font)
        self.search.setObjectName("search")
        
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setPlaceholderText("Enter search term...")
        self.searchBar.setGeometry(QtCore.QRect(200, 190, 160, 41))

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1203, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.charger.clicked.connect(self.Ouvrir)
        self.charger_desc.clicked.connect(self.loadFeatures)
        self.search.clicked.connect(self.loadFeaturesText)
        self.chargerText.clicked.connect(self.OuvrirText)
        self.chercher.clicked.connect(self.Recherche)
        self.calcul_RP.clicked.connect(self.rappel_precision )
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
        self.checkBox_LBP.setText(_translate("MainWindow", "LBP"))
        self.checkBox_HOG.setText(_translate("MainWindow", "HOG"))
        self.checkBox_Moments.setText(_translate("MainWindow", "Mom."))
        self.label_2.setText(_translate("MainWindow", "Image requête"))
        self.label_4.setText(_translate("MainWindow", "Recherche"))
        self.label_5.setText(_translate("MainWindow", "Rappel/Précision"))
        self.Quitter.setText(_translate("MainWindow", "Quitter"))
        self.label_7.setText(_translate("MainWindow", "Distance :"))
        self.recherche_sur.setText(_translate("MainWindow", "Recherche Sur :"))
        self.checkBox_Image.setText(_translate("MainWindow", "Image"))
        self.checkBox_Text.setText(_translate("MainWindow", "Text"))
        self.top_show.setText(_translate("MainWindow", "Top :"))
        self.label_8.setText(_translate("MainWindow", "Résultats"))
        self.label_9.setText(_translate("MainWindow", "Courbe R/P"))
        self.chercher.setText(_translate("MainWindow", "Recherche"))
        self.calcul_RP.setText(_translate("MainWindow", "Calculer la courbe R/P"))
        self.resultAP.setText(_translate("MainWindow", "Calcul de AP :"))
        self.resultMaP.setText(_translate("MainWindow", "Calcul de MaP :"))
        self.resultRP.setText(_translate("MainWindow", "Calcul de RP :"))
        self.checkBox_autre.setText(_translate("MainWindow", "Autre"))
        self.charger.setText(_translate("MainWindow", "Charger Image"))
        self.chargerText.setText(_translate("MainWindow", "Charger Text"))
        self.label_3.setText(_translate("MainWindow", "Requête"))
        self.charger_desc.setText(_translate("MainWindow", "Charger descripteurs"))
        self.search.setText(_translate("MainWindow", "Search"))


    def Ouvrir(self, MainWindow): 
        global fileName 
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "","Image Files (*.png *.jpeg *.jpg *.bmp)") 
        pixmap = QtGui.QPixmap(fileName) 
        pixmap = pixmap.scaled(self.label_requete.width(), 
        self.label_requete.height(), QtCore.Qt.KeepAspectRatio) 
        self.label_requete.setPixmap(pixmap) 
        self.label_requete.setAlignment(QtCore.Qt.AlignCenter)
    
    def OuvrirText(self, MainWindow): 
        global fileName 
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "","Image Files (*.png *.jpeg *.jpg *.bmp)") 
        pixmap = QtGui.QPixmap(fileName) 
        pixmap = pixmap.scaled(self.label_requete.width(), 
        self.label_requete.height(), QtCore.Qt.KeepAspectRatio) 
        self.label_requete.setPixmap(pixmap) 
        self.label_requete.setAlignment(QtCore.Qt.AlignCenter)
    
    def loadFeaturesText(self, MainWindow):
        folder_model = ""
    
        
    def loadFeatures(self, MainWindow):
        folder_model = ""
        
        if self.checkBox_HistC.isChecked():
            folder_model = './BGR'
            self.algo_choice = 1
        if self.checkBox_HSV.isChecked():
            folder_model = './HSV'
            #functions_recherche.generateHistogramme_HSV(filenames, self.progressBar)
            self.algo_choice = 2
        if self.checkBox_SIFT.isChecked():
            folder_model = './SIFT'
            #functions_recherche.generateSIFT(filenames, self.progressBar)
            self.algo_choice = 3
        if self.checkBox_ORB.isChecked():
            folder_model = './ORB'
            #functions_recherche.generateORB(filenames, self.progressBar)
            self.algo_choice = 4
        if self.checkBox_GLCM.isChecked():
            folder_model = './GLCM'
            #functions_recherche.generateGLCM(filenames, self.progressBar)
            self.algo_choice = 5
        if self.checkBox_HOG.isChecked():
            folder_model = './HOG'
            #functions_recherche.generateGLCM(filenames, self.progressBar)
            self.algo_choice = 6
        if self.checkBox_LBP.isChecked():
            folder_model = './LBP'
            #functions_recherche.generateLBP(filenames, self.progressBar)
            self.algo_choice = 7
        # Nettoyage du layout
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
    
        # Configuration du comboBox en fonction de l'algorithme choisi
        if filenames:
            if self.algo_choice in [3, 4]:  # SIFT et ORB
                self.comboBox.clear()
                self.comboBox.addItems(["Brute force", "Flann"])
            else:
                self.comboBox.clear()
                self.comboBox.addItems(["Euclidienne", "Correlation", "Chi carre", "Intersection", "Bhattacharyya"])
        if filenames:
            self.comboBoxTop.addItems(["Top20", "Top50"])
    
        if len(filenames) < 1:
            print("Merci de charger une image avec le bouton Ouvrir")
            return
    
        # Chargement des features
        self.features1 = []
        pas = 0
        print("Chargement des descripteurs en cours ...")
    
        if not os.path.exists(folder_model):
            print(f"Erreur : le dossier {folder_model} n'existe pas !")
            return
        total_files = sum(1 for _, _, files in os.walk(folder_model) for file in files if file.endswith(".txt"))
        for root, _, files in os.walk(folder_model):  # Parcours récursif
            for file in files:
                if not file.endswith(".txt"):
                    continue
                
                feature_path = os.path.join(root, file)
                feature = np.loadtxt(feature_path)
                
                image_name = os.path.basename(file).split('.')[0] + '.jpg'
                image_path = os.path.join(filenames, image_name)
    
                self.features1.append((image_path, feature))
    
                pas += 1
                self.progressBar.setValue(int(100 * ((pas + 1) / total_files)))
    
        # if not any([self.checkBox_SIFT.isChecked(), self.checkBox_HistC.isChecked(), 
        #             self.checkBox_HSV.isChecked(), self.checkBox_ORB.isChecked()]):
        #     print("Merci de sélectionner au moins un descripteur dans le menu")
        #     showDialog()
    
        print(len(self.features1))
        
    def Recherche(self, MainWindow):
        # Remise à 0 de la grille des voisins
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
            voisins = ""
    
        if self.algo_choice != 0:
            # Générer les features de l'image requête
            req = extractReqFeatures(fileName, self.algo_choice)
            # Définition du nombre de voisins
            if self.comboBoxTop.currentText() == "Top20":
                self.sortie = 20
            if self.comboBoxTop.currentText() == "Top50":
                self.sortie = 50 
            # Aller chercher dans la liste de l'interface la distance choisie
            distanceName = self.comboBox.currentText()
            # Générer les voisins
            voisins = getkVoisins(self.features1, req, self.sortie, distanceName)
            self.path_image_plus_proches = []
            self.nom_image_plus_proches = []
            
            base_path = os.path.dirname(os.path.abspath(__file__))  # Récupérer le dossier du script
            base_path = os.path.join(base_path, "MIR_DATASETS_B")  # Construire le chemin vers MIR_DATASETS_B
            
            for k in range(self.sortie):
                chemin_relatif = voisins[k][0]
                image_name = chemin_relatif.split('/')[-1]
                chemin_parts = chemin_relatif.split("_")
                if len(chemin_parts) >= 4:
                    categorie = chemin_parts[4]  # chiens, poissons ou singes
                    race = chemin_parts[5]  # race spécifique
                    chemin_complet = os.path.join(base_path, categorie, race, image_name)
                else:
                    print(f"Erreur : Format de chemin invalide pour {chemin_complet}")
                    continue
                
                self.path_image_plus_proches.append(chemin_complet)
                self.nom_image_plus_proches.append(image_name)
            
            # Nombre de colonnes pour l'affichage
            col = 3
            k = 0
            
            for i in range(math.ceil(self.sortie / col)):
                for j in range(col):
                    if k >= len(self.path_image_plus_proches):
                        break
                    
                    chemin_image = self.path_image_plus_proches[k]
                    
                    # Vérifier si le fichier existe
                    if not os.path.exists(chemin_image):
                        print(f"Erreur : L'image {chemin_image} n'existe pas. Vérifiez le chemin.")
                        k += 1
                        continue
                    
                    # Charger l'image
                    img = cv2.imread(chemin_image, cv2.IMREAD_COLOR)
                    if img is None:
                        print(f"Erreur : Impossible de charger {chemin_image}. Format non supporté ou fichier corrompu.")
                        k += 1
                        continue
                    
                    # Convertir en RGB
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
                    # Convertir en QImage
                    height, width, channel = img.shape
                    bytesPerLine = 3 * width
                    qImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(qImg)
                    
                    label = QtWidgets.QLabel("")
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    label.setPixmap(pixmap.scaled(min(int(0.3 * width),150), min(150,int(0.3 * height)), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
                    self.gridLayout.addWidget(label, i, j)
                    
                    k += 1
        else:
            print("Il faut choisir une méthode !")

        

    def rappel_precision(self): 
        rappel_precision = [] 
        rappels = [] 
        precisions = [] 
        
        filename_req = os.path.basename(fileName)  # Extraire le nom de fichier de fileName
        match = filename_req.split("_")[4].split('.')[0]
        if match:
            classe_image_requete = int(match) / 100  # Calcul de la classe de l'image requête
        else:
            print(f"Erreur : Impossible d'extraire un numéro valide de {match}")
            return  # Sortir de la fonction si l'extraction échoue
    
        val = 0 
        # Comparer les classes pour chaque voisin
        for j in range(self.sortie): 
            
            classe_image_proche = int(self.nom_image_plus_proches[j].split('_')[4].split('.')[0]) / 100
            if classe_image_requete == classe_image_proche: 
                rappel_precision.append(1)  # Bonne classe (pertinent) 
                val += 1 
            else: 
                rappel_precision.append(0)  # Mauvaise classe (non pertinent) 
    
        # Calcul des rappels et des précisions
        for i in range(self.sortie): 
            val = 0
            j = i
            while j >= 0: 
                if rappel_precision[j]: 
                    val += 1 
                j -= 1
            
            precision = val / (i + 1)  # Précision pour le voisin i
            rappel = val / sum(rappel_precision)  # Rappel pour le voisin i
            
            rappels.append(rappel)
            precisions.append(precision)
        
        # Création de la courbe R/P
        plt.plot(rappels, precisions) 
        plt.xlabel("Recall") 
        plt.ylabel("Precision") 
        plt.title(f"R/P {self.sortie} voisins de l'image n°{match}") 
    
        # Enregistrement de la courbe R/P
        save_folder = os.path.join(".", match)
        if not os.path.exists(save_folder): 
            os.makedirs(save_folder) 
        
        save_name = os.path.join(save_folder, f'{match}.png') 
        plt.savefig(save_name, format='png', dpi=600) 
        plt.close()  # Fermer la figure pour libérer les ressources
    
        # Affichage de la courbe R/P
        img = cv2.imread(save_name, 1)  # Charger l'image en couleur 
        b, g, r = cv2.split(img)  # Séparer les canaux
        img = cv2.merge([r, g, b])  # Convertir en RGB
        
        # Convertir l'image en QImage pour l'affichage dans l'interface
        height, width, channel = img.shape 
        bytesPerLine = 3 * width 
        qImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888) 
        pixmap = QtGui.QPixmap.fromImage(qImg) 
        
        # Ajuster l'image dans la taille du label
        width = self.label_requete.frameGeometry().width() 
        height = self.label_requete.frameGeometry().height() 
        
        self.label_courbe.setAlignment(QtCore.Qt.AlignCenter) 
        self.label_courbe.setPixmap(pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        
    def average_precision(rappels, precisions):
        """
        Calcule l'Average Precision (AP) en intégrant la courbe de précision-rappel.
        """
        if not rappels or not precisions:
            return 0.0
        
        rappels = np.array(rappels)
        precisions = np.array(precisions)
        
        # Tri des rappels et précisions
        sorted_indices = np.argsort(rappels)
        rappels = rappels[sorted_indices]
        precisions = precisions[sorted_indices]
        
        # AP en intégrant la courbe
        ap = np.sum((rappels[1:] - rappels[:-1]) * precisions[1:])
        self.valeurAP.setText(f"average_precision = {ap}")
        return ap
    
    def mean_average_precision(liste_AP):
        """
        Calcule la Mean Average Precision (mAP) en moyennant les AP de plusieurs requêtes.
        """
        if not liste_AP:
            return 0.0
        self.valeurMaP.setText(f"mean_average_precision = {np.mean(liste_AP)}")
        return np.mean(liste_AP)
    
    
    def r_precision(rappel_precision, R):
        """
        Calcule la R-Precision : la précision au rang R (nombre d'éléments pertinents dans les R premiers résultats).
        """
        if R <= 0 or R > len(rappel_precision):
            return 0.0
        self.valeurRP.setText(f"rappel_precision = {sum(rappel_precision[:R]) / R}")
        return sum(rappel_precision[:R]) / R

        
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
