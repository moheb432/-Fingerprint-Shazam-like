from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import pyqtgraph as pg
import numpy as np
from pydub import AudioSegment
import imagehash
from imagehash import hex_to_hash
from PIL import Image
import librosa as lib
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
from similarity import *

class Ui_mainwindow(object):
    
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(550, 470, 93, 28))
        self.reset.setObjectName("reset")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(660, 470, 93, 28))
        self.save.setObjectName("save")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 250, 701, 181))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(50, 40, 701, 194))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menufile.menuAction())
####################################################################


        self.save.clicked.connect(lambda:self.read())
        self.hashes=[]
        music= pd.read_excel('songsDataBase5.xlsx')
        self.DataB_songs = music[:].values    
        print(len(self.DataB_songs))     
####################moheb########################################3
        


        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.menufile.setTitle(_translate("MainWindow", "file"))

    def get_features(self,data,color,rate):
        return[lib.feature.mfcc(y=data.astype('float64'),sr=rate),
               lib.feature.melspectrogram(y=data,sr=rate,S=color),
               lib.feature.chroma_stft(y=data,sr=rate,S=color)]
    
    def PerHash(self,array):
        dataInstance = Image.fromarray(array)
        P_HASH= imagehash.phash(dataInstance, hash_size=16).__str__()
        
        return P_HASH

    def read(self):
        load_file = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File %s",filter="*.mp3")
        path=load_file[0]
        audiofile = AudioSegment.from_mp3(path)[:60000] 
        self.data = np.array(audiofile.get_array_of_samples())
        self.rate = audiofile.frame_rate
        print(self.data)
        self.spect()    
        self.compare()
        
    def spect(self):
            sampleFreqs,sampleTime, colorMesh = signal.spectrogram(self.data,fs=self.rate)
            self.test_spect_hash=self.PerHash(colorMesh)
            self.hashes.append(self.test_spect_hash)
            for fet in self.get_features(self.data,colorMesh,self.rate):
                self.hashes.append(self.PerHash(fet))
            
            print(self.hashes)
    def compare(self):
        self.all_similarity_index = similarity(self.DataB_songs,self.hashes)
        self.ui_table()

    def ui_table(self): 
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_mainwindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())    