from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import pyqtgraph as pg
from perceptial_hash import per_spec_hashs,mix
import pandas as pd
import matplotlib.pyplot as plt
from sim_index import similarity
import numpy as np
from pydub import AudioSegment
from scipy import signal

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
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.slider1 = QtWidgets.QSlider(self.widget)
        self.slider1.setSliderPosition(40)
        self.slider1.setOrientation(QtCore.Qt.Vertical)
        self.slider1.setObjectName("slider1")
        self.slider1.setMaximum(100)
        self.slider1.setMinimum(0)
        
        
        self.horizontalLayout.addWidget(self.slider1)
####################################################################
        
        self.save.clicked.connect(lambda:self.read(1))
        self.reset.clicked.connect(lambda:self.read(2))
        self.slider1.sliderReleased.connect(lambda:self.func_mixer())
        self.hashes=[]
        self.mixer=[]
        self.slider1.hide()
        music= pd.read_csv('musics.csv')
        self.DataB_songs = music[:].values    
        self.musics_names=[]
        for i in range(0,len(self.DataB_songs)):
            self.musics_names.append([self.DataB_songs[i][0]])   
        
####################moheb########################################3
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.menufile.setTitle(_translate("MainWindow", "file"))

    def read(self,temp):
        load_file = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File %s",filter="*.mp3")
        path=load_file[0]
        audiofile = AudioSegment.from_mp3(path)[:60000] 
        self.data = np.array(audiofile.get_array_of_samples())
        self.rate = audiofile.frame_rate
        self.mixer.append(self.data)
        if temp==1:
            hashes=per_spec_hashs(self.data,self.rate)    
            self.compare(hashes)
        if temp==2:
            self.slider1.show()
            pass
        
    def compare(self,hashes):
        print(hashes)
        similarity_index = similarity(self.DataB_songs,hashes)
        print(similarity_index)
        self.musics=[]
            
        for i in range(0,len(self.musics_names)):
                self.musics.append([self.musics_names[i][0],similarity_index[i]])
        # print(self.musics)
        self.ui_table()
        
    def func_mixer(self):
        data = mix(self.mixer[0] ,self.mixer[1][0:len(self.mixer[0])],self.slider1.value()/100)
        hashes=per_spec_hashs(data,self.rate)
        
        self.compare(hashes)
   
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