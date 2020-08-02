import os
import glob
import shutil
import mosspy
import zipfile
import itertools
from pathlib import Path

class Moss():
    def __init__(self, mossfolderpath, students):
        self.mossfolderpath = mossfolderpath
        self.students = students
    
    def create_moss_folder():
        #for cpp
        folder_path = str(self.mossfolderpath) + r'\mosscpp'
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        for i in range(len(self.students)):
            self.students[i].cpp_grade.moss_id = i
            Path(folder_path + fr'\{i}').mkdir(parents=True, exist_ok=True)
            shutil.copytree(self.students[i].cpp_grade.best_path, folder_path + fr'\{i}')
        #for python
        folder_path = str(self.mossfolderpath) + r'\mosspython'
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        for i in range(len(self.students)):
            self.students[i].python_grade.moss_id = i
            Path(folder_path + fr'\{i}').mkdir(parents=True, exist_ok=True)
            shutil.copytree(self.students[i].cpp_grade.best_path, folder_path + fr'\{i}')

    def run_moss():
        current = os.getcwd()
        self.create_moss_folder()
        userid = 360162800
        m = mosspy.Moss(userid, "python")
        
        #cpp moss
        os.chdir(self.mossfolderpath + r'\mosscpp')
        for stu in os.listdir(os.getcwd()):     #moss id  of courses for each student
            stu = os.path.abspath(stu)
            for best_sub in os.listdir(stu):
                for cpps in os.listdir(best_sub):
                    stusubs = stu + fr'{best_sub}\cpp\{cpps}'
                    m.addFile(stusubs)
        url = m.send() 
        m.saveWebPage(url, "submission/cppreport.html")     # Save report file
        # mosspy.download_report(url, "submission/cppreport/", connections=8, log_level=10) # logging.DEBUG (20 to disable)

        #python moss
        os.chdir(self.mossfolderpath + r'\mosspython')
        for stu in os.listdir(os.getcwd()):     #moss id  of courses for each student
            stu = os.path.abspath(stu)
            for best_sub in os.listdir(stu):
                for cpps in os.listdir(best_sub):
                    stusubs = stu + fr'{best_sub}\cpp\{cpps}'
                    m.addFile(stusubs)
        url = m.send() 
        m.saveWebPage(url, "submission/pythonreport.html")      # Save report file
        # mosspy.download_report(url, "submission/pythonreport/", connections=8, log_level=10) # logging.DEBUG (20 to disable)

        os.chdir(current)


