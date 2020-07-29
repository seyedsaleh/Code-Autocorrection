import os
import re
import numbers
# import subprocess
import numpy as np

class student():
    def __init__(self, setting_Data, folder_Address, cpp_testlist, python_testlist, cpp_each_test_grade, python_each_test_grade):
        self.setting_data = setting_Data
        self.folder_address = folder_Address
        self.cpp_testlist = cpp_testlist
        self.python_testlist = python_testlist
        self.cpp_each_test_grade = cpp_each_test_grade
        self.python_each_test_grade = python_each_test_grade
        self.folder_name = os.path.basename(folder_Address)
        self.farsi_name = ''
        self.eng_name = ''
        self.student_id = 0  

        self.grades = []                    #key: number of test, value: point loss of that test. (?!)
        self.build_okay = 0                 # 1 if built successfully.
        self.report_name_format = 0         # 1 if the report name format is okay.
        self.folder_name_format = 0         # 1 if the folder name format is okay.
        self.warnings = []                  #key: number of test, value: warning (string)
        self.images = []                    #key: number of test, value: image (string)
        self.builds = []
        self.python_beauty = 0
        #self.moss = None
        self.final_grade = 0


    def check_format(self, name):                                      #the name must be in shape "MohammadMahdiShojaefar9623065"
        if len(name) < 7 :
            return False
        if ((name[-7:]).isnumeric() and (name[:-7]).isalpha()):
            return name[:-7], name[-7:]
        elif ((name[-8:]).isnumeric() and (name[:-8]).isalpha()):
            return name[:-8], name[-8:]
        return False

    def get_name(self):                                           #path of 'xxxxx_name_assi...sub..._file_' in hw
                                                                   #before this func must check the foldar that contain CPlusPlus or Python
        pdfname = []
        subname = []
        temp = []
        os.chdir(folder_Address)
        s = os.path.basename(folder_Address)
        for ch in s:
            if not(ch>='a' and ch<='z') and not(ch>='A' and ch<='Z') and not(ch>='0' and ch<='9') and ch != '_':
                temp.append(ch)
        subname.append(''.join(map(str, temp)))
        current_path = os.path.abspath(os.getcwd())
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file[-4:] == '.pdf':
                    pdfname.append(file[:-4])
        if os.path.exists('CPlusPlus'):
            os.chdir('CPlusPlus')
        else:
            os.chdir('Python')
        for file in os.listdir(str(os.getcwd())):
            if file[:7] != 'Answer_':
                subname.append(file)
        os.chdir(current_path)
        return pdfname, subname

    def pre_process(self):
        pdfname, subname = self.get_name()
        self.farsi_name = subname[0] 
        for name in pdfname:
            if self.check_format(name) != False:
                self.report_name_format = 1
                self.eng_name, self.student_id = self.check_format(name)
        for name in subname:
            if self.check_format(name) != False:
                self.folder_name_format = 1
                self.eng_name, self.student_id = self.check_format(name)

    def findwarning(s):                                         #s is string of warnings
        warning_list = []
        s = s.lower()
        while s.find("warning") != -1:
            temp1 = s[:s.rfind("warning")]
            temp = s[temp1.rfind("\n")+1:]
            warning = temp[:temp.find("\n")]
            s = s.replace(warning,'')
            # print(warning)
            warning_list.append(warning)   
        return warning_list

    def grade_cppfolder(self, s):                               #s is in shape "CPlusPlus\Answer_name\name_i"
        current_path = os.path.abspath(os.getcwd())
        final_grade = []
        warning_list = []
        img_list = []
        build_list = []
        os.chdir(s)                                             #first we create test list, then we grade the code
        #open unittest and clear all tests
        with open(r'cpp\aphw_unittest.cpp', "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(self.cpp_testlist[-2][0])
            f.truncate()
        xxx = np.random.randint(1000000)
        stop = os.popen('docker stop hw1').read()
        # os.system('docker build --no-cache -t ap1398/hw1 .')
        ans = os.popen(f'docker build -t ap1398/hw{xxx} --build-arg CACHEBUST=1 .').read()   #12/12 ...check the code is ok or not
        # print(ans)
        build_list.append([-1, ans])
        warning_list = self.findwarning(ans)                    #create warning list
        if( ans.find('Successfully built') == -1):              #it happens when the code cant compile correctly, so the final grade is zero
            final_grade = [[i+1,'Compile Error All'] for i in range(len(self.cpp_testlist)-2)]
        else:                                                   #now we grade each test
            for i in range(len(self.cpp_testlist)-2):
                #change unittest to grade each test
                with open(r'cpp\aphw_unittest.cpp', "r+") as f:
                    data = f.read()
                    f.seek(0)
                    f.write(self.cpp_testlist[i][0])
                    f.truncate()

                stop = os.popen('docker stop hw1').read()
                # os.system('docker build -t ap1398/hw1 .')
                ans = os.popen(f'docker build -t ap1398/hw{xxx} .').read()    #12/12 ...
                build_list.append([self.cpp_testlist[i][1], ans])
                if( ans.find('Successfully built') != -1):      #it happens when the code can't compile correctly, so the grade of this test is zero
                    # warning_list.append([test_list[i][1], findwarning(ans)])
                    img = os.popen(f'docker run --rm ap1398/hw{xxx}').read() #when the code compile correctlr, we check the result
                    img_list.append([self.cpp_testlist[i][1], img])
                    # print(ans)#show warning
                    # print(img)
                    if img.find('<<<SUCCESS>>>') != -1:         #passed
                        final_grade.append([self.cpp_testlist[i][1],0])
                    else:
                        ansg = 0
                        numinus = len(re.findall('minus', img)) #get num of failed test(EXPECT_EQ)
                        while numinus > 0:
                            minustr = img[img.rfind("minus"):]
                            minus = re.findall(r'[-+]?\d*\.\d+|\d+', minustr)[0]    #find the grade of each test(EXPECT_EQ)
                            ansg += float(minus)
                            img = img.replace(minustr, '')
                            numinus -= 1
                        final_grade.append([self.cpp_testlist[i][1],ansg])          #failed
                else:
                    final_grade.append([self.cpp_testlist[i][1],'Compile Error'])   #copmile error

        with open(r'cpp\aphw_unittest.cpp', "r+") as f:        #change unittest to first manner
                    data = f.read()
                    f.seek(0)
                    f.write(self.cpp_testlist[-1][0])
                    f.truncate()
        os.chdir(current_path)
        # print(final_grade)
        # print(warning_list)
        return final_grade, warning_list, img_list, build_list  #ex for final grades: [[1,10],[2,0],[3,Compile Error],[4,10]]
                                                                #means test 1 and 4 passed and test 2 failed. test 3 had compile error

    def final_cppfolder_grade(self, folder_grades_list):
        final = 0
        for i in range(len(self.cpp_each_test_grade)):
            if isinstance(folder_grades_list[i][1], numbers.Number):
                final += cpp_each_test_grade[i][1]-folder_grades_list[i][1]
        return final

    def grading(self):
        self.build_okay = 0
        self.grades = {}
        self.warnings = {}
        self.images = {}

    def beauty_check(self):
        self.python_beauty = 0

    def final_grade(self):
        self.final_grade = 0

    def run_student(self):
        self.pre_process()
        self.grading()
        self.beauty_check()
        self.final_grade()

if __name__ == "__main__":
    print('ok')
