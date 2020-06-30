import os
import sys 

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from setting import *

#____________________________________________________________________________

mainWindow_form = uic.loadUiType(os.path.join(os.getcwd(), "gui_v1.ui"))[0]

class mainWindow(QMainWindow, mainWindow_form):
    def __init__(self):
        mainWindow_form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setting_window = settingWindow()

        self.treeView_model = QDirModel()
        self.testFiles_treeView.setModel(self.treeView_model)
        self.studentsFiles_treeView.setModel(self.treeView_model)
        file_path = os.getcwd()
        self.testFiles_treeView.setRootIndex(self.treeView_model.index(file_path))
        self.studentsFiles_treeView.setRootIndex(self.treeView_model.index(file_path))

        #Events
        self.action_setting.triggered.connect(self.open_setting)
        self.action_open_students_file.triggered.connect(self.open_students_file)
        self.action_open_test_file.triggered.connect(self.open_test_file)
    
    def open_setting(self):
        self.setting_window.show()
    
    def open_students_file(self):
        print("student file ok")
        file_path =  QFileDialog.getOpenFileName(self, "Open Students File")[0]  
        self.testFiles_treeView.setRootIndex(self.treeView_model.index(file_path))  

    '''
    open_action = QAction("&Open")
    def open_file():
        global file_path
        path = QFileDialog.getOpenFileName(window, "Open")[0]
        if path:
            text.setPlainText(open(path).read())
            file_path = path
    '''

    def open_test_file(self):
        print("test file ok")

#____________________________________________________________________________

app = QApplication([])
app.setStyle("fusion")
w = mainWindow()
w.show()
#w2 = settingWindow()
#w2.show()
sys.exit(app.exec_())