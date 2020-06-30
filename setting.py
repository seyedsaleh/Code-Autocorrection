import os
import sys 

#from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence


#____________________________________________________________________________

settingWindow_form = uic.loadUiType(os.path.join(os.getcwd(), "setting_ui.ui"))[0]

class settingWindow(QMainWindow, settingWindow_form):
    def __init__(self):
        settingWindow_form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)

        #Events
        self.gs_beauty_hSlider.valueChanged.connect(self.update_gs_beauty)

    def update_gs_beauty(self, val):
        self.gs_beauty_label2.setText(str(val))