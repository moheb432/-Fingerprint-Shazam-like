from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMainWindow
import os
from os import path
import logging
import pyqtgraph as pg
from hashing_m import per_spec_hashs,mix
import pandas as pd
import matplotlib.pyplot as plt
from similarity_m import similarity
import numpy as np
from pydub import AudioSegment
from scipy import signal
import operator



THIS_FOLDER= path.dirname(path.abspath(__file__))
FORM_CLASS,_=loadUiType(path.join(THIS_FOLDER, "shazam.ui"))



 
logging.basicConfig(filename='LogFile.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
#self.logger = logging.getLogger()
#self.logger.setLevel(logging.DEBUG)
 



class MainApp(QtWidgets.QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        self.starter_UI()
        
        
   
        
       
    
    
    
    def handle_UI(self):
         _translate = QtCore.QCoreApplication.translate
         self.loadmusic1.clicked.connect(lambda:self.music_load(1))
         self.loadmusic2.clicked.connect(lambda:self.music_load(2))
         self.mix_slider.sliderReleased.connect(lambda:self.func_mixer())
         
    def starter_UI(self):
         self.hashes=[]
         self.mixer=[]
         self.mix_slider.hide()
         self.label_3.hide()
         self.resultsTable.hide()
         music= pd.read_csv('musics.csv')
         self.DataB_songs = music[:].values    
         self.musics_names=[]
         for i in range(0,len(self.DataB_songs)):
            self.musics_names.append([self.DataB_songs[i][0]])
         self.reset.clicked.connect(lambda:self.reseT())   
        
        
        
        
    def music_load (self, action):
        load_file = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File %s",filter="*.mp3")
        path=load_file[0]
        audiofile = AudioSegment.from_mp3(path)[:60000] 
        self.data = np.array(audiofile.get_array_of_samples())[0:5000000]
        self.rate = audiofile.frame_rate
        self.mixer.append(self.data)
        if action==1:
            hashes=per_spec_hashs(self.data,self.rate)    
            self.compare(hashes)
        if action==2:
            self.mix_slider.show()
            self.label_3.show()
            pass
        
        
    def compare(self,hashes):
        self.similarity_index = similarity(self.DataB_songs,hashes)
        self.musics=[]
        self.sortedMusics=[]
            
        for i in range(0,len(self.musics_names)):
                self.musics.append([self.musics_names[i][0],self.similarity_index[i]])
        
        self.sortedMusics= sorted(self.musics, key=operator.itemgetter(1), reverse=True)

        self.ui_table()
        
        
    def func_mixer(self):
        data = mix(self.mixer[0] ,self.mixer[1],self.mix_slider.value()/100)
        hashes=per_spec_hashs(data,self.rate)
        self.compare(hashes)
    
    def reseT(self):
          self.resultsTable.hide()
          self.resultsTable.clear()
          self.mixer.clear()
    def ui_table(self): 
        # pass
        self.resultsTable.setColumnCount(2)
        self.resultsTable.setRowCount(len(self.sortedMusics))

        for row in range(len(self.musics)):
            self.resultsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(self.sortedMusics[row][0]))
            self.resultsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(self.sortedMusics[row][1], 2))+"%"))
            self.resultsTable.item(row, 0).setBackground(QtGui.QColor(57, 65, 67))
            self.resultsTable.item(row, 1).setBackground(QtGui.QColor(57, 65, 67))
            self.resultsTable.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.Stretch)

        self.resultsTable.setHorizontalHeaderLabels(["Song_Name", "Similarity"])

        for col in range(2):
            self.resultsTable.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            self.resultsTable.horizontalHeaderItem(col).setBackground(QtGui.QColor(57, 65, 67))

        self.resultsTable.show()

        self.similarity_index.clear()
        
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window= MainApp()
    window.show()  
    app.exec_()
    


if __name__ == '__main__':
    main()
        
        
        
        
        