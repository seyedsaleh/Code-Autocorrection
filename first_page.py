import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QAbstractItemView

from Directory import Directory
from setting_window import SettingWindow
from PyQt5.QtCore import QModelIndex


firstPageForm = uic.loadUiType(os.path.join(os.getcwd(), "dlg_first_page.ui"))[0]



class Firstpage(QMainWindow, firstPageForm):
    def __init__(self):
        firstPageForm.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.ok_icon = QIcon(os.path.join(os.getcwd(), "rc/emblem-checked.png"))
        self.error_icon = QIcon(os.path.join(os.getcwd(), "rc/emblem-important.png"))

        self.directory = None

        self.entry = QStandardItemModel()
        self.listView.setModel(self.entry)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Events
        self.openStdButton.clicked.connect(self.open_std_file)
        self.openCppTestButton.clicked.connect(self.open_cpp_test_folder)
        self.openPythonTestButton.clicked.connect(self.open_python_test_folder)

        # Setting Window
        self.setting_window = SettingWindow()

        self.settingButton.clicked.connect(self.open_setting)
        self.setting_window.ok_Button.clicked.connect(self.setting_button_callback)
        self.setting_window.cancel_Button.clicked.connect(self.setting_button_callback)

        self.startButton.clicked.connect(self.start)

    def open_std_file(self):
        self.stdPath = QFileDialog.getOpenFileName(self, "Open a file")[0]
        self.entry.appendRow(QStandardItem(self.ok_icon, "Student file ok..."))

    def open_cpp_test_folder(self):
        self.cppTestPath = QFileDialog.getExistingDirectory(self, "Select a folder:", os.getcwd(),
                                                            QFileDialog.ShowDirsOnly)
        self.entry.appendRow(QStandardItem(self.ok_icon, "Cpp test file ok..."))

    def open_python_test_folder(self):
        self.pythonTestPath = QFileDialog.getExistingDirectory(self, "Select a folder:", os.getcwd(),
                                                               QFileDialog.ShowDirsOnly)
        self.entry.appendRow(QStandardItem(self.ok_icon, "Python test file ok..."))

    def open_setting(self):
        self.setting_window.show()
        self.setting_window.set_initial_values()

    def setting_button_callback(self):
        self.setting_window.close()

    def start(self):
        self.directory = Directory(self, self.setting_window.setting_data, self.stdPath, self.cppTestPath,
                                   self.pythonTestPath)
        self.directory.display_signal.connect(self.test)
        self.directory.start()

    def test(self, *val):
        if val[1]:
            self.entry.appendRow(QStandardItem(self.ok_icon, val[0]))
        else:
            self.entry.appendRow(QStandardItem(self.error_icon, val[0]))


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle("fusion")
    w = Firstpage()
    w.show()
    sys.exit(app.exec_())
