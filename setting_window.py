import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from Setting import Setting

settingWindow_form = uic.loadUiType(os.path.join(os.getcwd(), "dlg_setting_window.ui"))[0]


class SettingWindow(QMainWindow, settingWindow_form):

    def __init__(self):
        settingWindow_form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setting_data = Setting()

        self.setting_okay_flag = 0

        # Events
        # grading setting events
        self.gs_beauty_hSlider.valueChanged.connect(self.update_gs_beauty)
        self.gs_report_hSlider.valueChanged.connect(self.update_gs_report)
        self.gs_test_1_spinBox.valueChanged.connect(self.update_test_1)
        self.gs_test_1_lineEdit.textChanged.connect(self.update_test_1)
        self.gs_test_2_spinBox.valueChanged.connect(self.update_test_2)
        self.gs_test_2_lineEdit.textChanged.connect(self.update_test_2)
        self.gs_file_names_lineEdit.textChanged.connect(self.update_file_names)
        self.gs_img_output_lineEdit.textChanged.connect(self.update_img_tests)
        # output setting events
        self.os_excel_checkBox.stateChanged.connect(self.update_excel_state)
        self.os_pdf_checkBox.stateChanged.connect(self.update_pdf_state)
        self.os_grade_checkBox.stateChanged.connect(self.update_output_type)
        self.os_mos_checkBox.stateChanged.connect(self.update_output_type)
        self.os_mos_grade_checkBox.stateChanged.connect(self.update_output_type)
        self.os_cheat_hSlider.valueChanged.connect(self.cheat_limit)
        self.os_pyDefault_radioButton.toggled.connect(self.PythonPython)
        # advance setting events
        self.adv_bulid_lineEdit.textChanged.connect(self.build_keyWord_update)
        self.adv_cppTest_lineEdit.textChanged.connect(self.cppTest_keyWord_update)
        self.adv_pyTest_lineEdit.textChanged.connect(self.pyTest_keyWord_update)
        self.adv_minus_lineEdit.textChanged.connect(self.minus_keyWord_update)

        self.ok_Button.clicked.connect(self.ok_button_callback)
        self.cancel_Button.clicked.connect(self.cancel_button_callback)

    def set_initial_values(self):
        self.gs_beauty_hSlider.setValue(25)
        self.gs_report_hSlider.setValue(5)

    # grading setting events
    def update_gs_beauty(self, val):
        self.gs_beauty_label2.setText(str(val))
        self.setting_data.beauty_coefficient = val

    def update_gs_report(self, val):
        self.gs_report_label2.setText(str(val))
        self.setting_data.report_coefficient = val

    def update_test_1(self, val):
        if isinstance(val, int):
            self.setting_data.test_1_number = val
        else:
            self.setting_data.test_1_point = val

    def update_test_2(self, val):
        if isinstance(val, int):
            self.setting_data.test_2_number = val
        else:
            self.setting_data.test_2_point = val

    def update_file_names(self, val):
        l = self.make_csv(val)
        self.setting_data.file_names = l

    def update_img_tests(self, val):
        l = self.make_csv(val)
        self.setting_data.img_tests = l

    # output setting events
    def update_pdf_state(self):
        if self.os_pdf_checkBox.isChecked():
            self.setting_data.pdf_output = 1
        else:
            self.setting_data.excel_output = -1

    def cheat_limit(self, val):
        if self.os_mos_grade_checkBox.isChecked():
            self.os_cheat_label.setText(str(val))
            self.setting_data.similarity_limit = val
        else:
            self.os_cheat_hSlider.setValue(0)
            self.os_cheat_label.setText("")
            self.setting_data.similarity_limit = -1

    def update_output_type(self):
        if self.os_grade_checkBox.isChecked():
            self.setting_data.grade_output = 1
        else:
            self.setting_data.grade_output = -1

        if self.os_mos_checkBox.isChecked():
            self.setting_data.mos_output = 1
        else:
            self.setting_data.mos_output = -1

        if self.os_mos_grade_checkBox.isChecked():
            self.setting_data.grade_mos_output = 1
        else:
            self.setting_data.grade_mos_output = -1
            self.os_cheat_hSlider.setValue(0)
            self.os_cheat_label.setText("")
            self.setting_data.similarity_limit = -1

    def update_excel_state(self):
        if self.os_excel_checkBox.isChecked():
            self.setting_data.excel_output = 1
        else:
            self.setting_data.excel_output = -1

    def PythonPython(self):
        if self.os_pyDefault_radioButton.isChecked():
            self.setting_data.python_python = 0
        else:
            self.setting_data.python_python = 1  # default is Docker.

    # advance setting events
    def minus_keyWord_update(self, val):
        self.setting_data.minus_keyWord = val

    def pyTest_keyWord_update(self, val):
        self.setting_data.pyTest_keyWord = val

    def cppTest_keyWord_update(self, val):
        self.setting_data.cppTest_keyWord = val

    def build_keyWord_update(self, val):
        self.setting_data.build_keyWord = val

    # okay / cancel
    def ok_button_callback(self):
        self.setting_data.show()
        self.setting_okay_flag = 1

    def cancel_button_callback(self):
        self.gs_beauty_hSlider.setValue(0)
        self.gs_report_hSlider.setValue(0)
        self.gs_test_1_spinBox.setValue(0)
        self.gs_test_1_lineEdit.setText("")
        self.gs_test_2_spinBox.setValue(0)
        self.gs_test_2_lineEdit.setText("")
        self.gs_file_names_lineEdit.setText("")
        self.gs_img_output_lineEdit.setText("")

        self.os_cheat_hSlider.setValue(0)
        self.os_cheat_label.setText("")
        self.os_excel_checkBox.setChecked(False)
        self.os_pdf_checkBox.setChecked(False)
        self.os_pyDocker_radioButton.setChecked(True)
        self.os_mos_checkBox.setChecked(False)
        self.os_mos_grade_checkBox.setChecked(False)
        self.os_grade_checkBox.setChecked(False)

        self.adv_bulid_lineEdit.setText("Successfully built")
        self.adv_cppTest_lineEdit.setText("<<<success>>>")
        self.adv_pyTest_lineEdit.setText("Failure")
        self.adv_minus_lineEdit.setText("minus")

        self.setting_data.set_to_none()
        self.setting_data.show()

        self.setting_okay_flag = 0

    @staticmethod
    def make_csv(str):
        return list(map(lambda s: s.strip(), str.split(',')))
