import os
import re
import shutil
import mosspy
from pathlib import Path

class Moss():
    def __init__(self, lang, mossfolderpath, students):
        self.mossfolderpath = mossfolderpath
        self.students = students
        self.cpp_exist = lang[0]
        self.python_exist = lang[1]
    
    def create_moss_folder(self):
        #for cpp
        if self.cpp_exist:
            folder_path = str(self.mossfolderpath) + r'\mosscpp'
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            for i in range(len(self.students)):
                self.students[i].cpp_grade.moss_id = i
                Path(folder_path + fr'\mossid_{i}').mkdir(parents=True, exist_ok=True)
                basename = os.path.basename(self.students.cpp_grade.best_path)
                shutil.copytree(self.students[i].cpp_grade.best_path, folder_path + fr'\mossid_{i}\{basename}')
        #for python
        if self.python_exist:
            folder_path = str(self.mossfolderpath) + r'\mosspython'
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            for i in range(len(self.students)):
                self.students[i].python_grade.moss_id = i
                Path(folder_path + fr'\mossid_{i}').mkdir(parents=True, exist_ok=True)
                basename = os.path.basename(self.students.cpp_grade.best_path)
                shutil.copytree(self.students[i].cpp_grade.best_path, folder_path + fr'\mossid_{i}\{basename}')

    def run_moss(self):
        current = os.getcwd()
        self.create_moss_folder()
        userid = 360162800
        m = mosspy.Moss(userid, "python")
        #cpp moss
        if self.cpp_exist:
            os.chdir(self.mossfolderpath + r'\mosscpp')
            for stu in os.listdir(os.getcwd()):     #moss id  of courses for each student
                stu = os.path.abspath(stu)
                for best_sub in os.listdir(stu):
                    for cpps in os.listdir(best_sub):
                        stusubs = stu + fr'{best_sub}\cpp\{cpps}'
                        m.addFile(stusubs)
            url = m.send() 
            m.saveWebPage(url, "cppreport.html")     # Save report file
        #python moss
        if self.python_exist:
            os.chdir(self.mossfolderpath + r'\mosspython')
            for stu in os.listdir(os.getcwd()):     #moss id  of courses for each student
                stu = os.path.abspath(stu)
                for best_sub in os.listdir(stu):
                    for cpps in os.listdir(best_sub):
                        stusubs = stu + fr'{best_sub}\cpp\{cpps}'
                        m.addFile(stusubs)
            url = m.send() 
            m.saveWebPage(url, "pythonreport.html")      # Save report file
        os.chdir(current)

    def check_report(self, name):
        current = os.getcwd()
        os.chdir(self.mossfolderpath)
        with open(name, 'r') as rp:
            report = rp.read() 
        r1 = re.findall(r"(\W+\d+\W+\b)", report)
        l = []
        for i in r1:
            if i.startswith(" ("):
                ii = i.replace('</', '')
                iii = ii.replace('(', '')
                iiii = iii.replace(')', '')
                iiiii = iiii.replace('%', '')
                l.append(int(iiiii))
        l2 = [i for i in l if i > 50]
        l3 = [f'({i}%)' for i in l2]
        N = report.find("<TABLE>")
        N2 = report.find("</TABLE>")
        report2 = report[N+8:N2]
        report_list = report2.split('\n')
        L = [i for i in report_list]
        L3 = []
        for i in l3:
            for j in L:
                if i in j:
                    L3.append(j)
                    break
        final_result = []
        for i in L3:
            n = i.find('mossid_')
            n2 = i[n:].find('/')
            final_result.append(i[n:n+n2])
            # print(i, '\n')
            # print(i[n:n+n2])
        print(final_result)
        print(l3)
        final_result_index = []
        for num in final_result:
            for i in range(len(self.students)):
                if self.students[i].cpp_grade.moss_id == num:
                    final_result_index.append(i)
        os.chdir(current)        
        return final_result, l3, final_result_index

    def update_student(self):
        self.run_moss()
        cpp_final_result, cpp_percent, cpp_final_result_index = self.check_report("cppreport.html")
        for i in range(0, len(cpp_final_result), 2):
            ind1 = cpp_final_result_index[i]
            ind2 = cpp_final_result_index[i+1]
            self.students[ind1].cpp_grade.moss = True
            self.students[ind2].cpp_grade.moss = True

            self.students[ind1].cpp_grade.moss_percent.append(cpp_percent[ind1])
            self.students[ind1].cpp_grade.moss_percent.append(cpp_percent[ind2])

            self.students[ind1].cpp_grade.moss_student.append(self.students[ind2].farsi_name)
            self.students[ind2].cpp_grade.moss_student.append(self.students[ind1].farsi_name)

        python_final_result, python_percent, python_final_result_index = self.check_report("pythonreport.html")
        for i in range(0, len(python_final_result), 2):
            ind1 = python_final_result_index[i]
            ind2 = python_final_result_index[i+1]
            self.students[ind1].python_grade.moss = True
            self.students[ind2].python_grade.moss = True

            self.students[ind1].python_grade.moss_percent.append(python_percent[ind1])
            self.students[ind1].python_grade.moss_percent.append(python_percent[ind2])
            
            self.students[ind1].python_grade.moss_student.append(self.students[ind2].farsi_name)
            self.students[ind2].python_grade.moss_student.append(self.students[ind1].farsi_name)
