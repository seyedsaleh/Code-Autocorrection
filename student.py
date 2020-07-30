import re
import os
import numbers
import subprocess
import numpy as np

class cppgrade():

    def __init__(self, setting_Data, folder_Address, cpp_testlist, cpp_each_test_grade):
        self.setting_data = setting_Data
        self.folder_address = folder_Address
        self.cpp_testlist = cpp_testlist
        self.cpp_each_test_grade = cpp_each_test_grade

        self.build_okay = 0                 # 1 if built successfully.
        self.grades = []                    #key: number of test, value: point loss of that test. (?!)
        self.warnings = []                  #key: number of test, value: warning (string)
        self.images = []                    #key: number of test, value: image (string)
        self.builds = []
        self.best_path = folder_Address     #best manner of submissions
        self.moss = None
        self.final_grade = 0
        # self.moss_id = 0

    def findwarning(self, s):                                   #s is string of warnings
        warning_list = []
        s = s.lower()
        while s.find("warning") != -1:
            temp1 = s[:s.rfind("warning")]
            temp = s[temp1.rfind("\n")+1:]
            warning = temp[:temp.find("\n")]
            s = s.replace(warning,'')
            warning_list.append(warning)   
        return warning_list

    def grade_folder(self, s):                                  #s is in shape "CPlusPlus\Answer_name\name_i"
        current_path = os.path.abspath(os.getcwd())
        final_grade = []
        warning_list = []
        img_list = []
        build_list = []
        os.chdir(s)                                             #first we create test list, then we grade the code
        # open unittest and clear all tests
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

    def final_folder_grade(self, folder_grades_list):
        final = 0
        for i in range(len(self.cpp_each_test_grade)):
            if isinstance(folder_grades_list[i][1], numbers.Number):
                final += self.cpp_each_test_grade[i][1]-folder_grades_list[i][1]
        return final

    def grading(self):                                          #only cpp grade
        all_output = []
        final_output = []
        current_path = os.getcwd()
        os.chdir(self.folder_address)
        if not os.path.exists('CPlusPlus'):
            os.chdir(current_path)
            return False

        os.chdir('CPlusPlus')
        print(os.getcwd())
        for subs in os.listdir(os.path.abspath(os.getcwd())):
            if subs[:7] == 'Answer_':
                for manner in os.listdir(os.path.abspath(subs)):
                    # print(os.getcwd()+fr'\{subs}\{manner}')
                    f_grade, w_list, i_list, b_list = self.grade_folder(os.getcwd()+fr'\{subs}\{manner}')
                    all_output.append([f_grade, w_list, i_list, b_list, os.path.abspath(manner)])
        for i in range(len(all_output)):
            if self.final_folder_grade(all_output[i][0]) > self.final_grade:
                self.final_grade = self.final_folder_grade(all_output[i][0])
                final_output = all_output[i]
        self.grades = final_output[0]
        self.warnings = final_output[1]
        self.images = final_output[2]
        self.builds = final_output[3]
        self.best_path = final_output[4]
        if len(self.builds) > 1:
            self.build_okay = 1

    # def run_student(self):
        # self.grading()


class pygrade():

    def __init__(self, setting_Data, folder_Address, python_testlist, python_each_test_grade):
        self.setting_data = setting_Data
        self.folder_address = folder_Address
        self.python_testlist = python_testlist
        self.python_each_test_grade = python_each_test_grade

        self.grades = []                    #key: number of test, value: point loss of that test. (?!)
        self.images = []                    #key: number of test, value: image (string)
        self.python_beauty = 0
        self.best_path = folder_Address
        self.moss = None
        self.moss_id = 0
        self.final_grade = -5

    def beauty_check(self):
        self.python_beauty = 0
    
    def grade_folder(self, s, docker_on = True):
        final_grade = []
        img_list = []
        current_path = os.path.abspath(os.getcwd())
        os.chdir(s)                                             #first we create test list, then we grade the code
        if docker_on == True:
            for i in range(len(self.python_testlist)-1):
                #change unittest to grade each test
                with open(r'aphw_unittest.py', "r+") as f:
                    data = f.read()
                    f.seek(0)
                    f.write(self.python_testlist[i][0])
                    f.truncate()

                # stop = os.popen('docker stop hw1').read()
                xxx = np.random.randint(1000000)
                ans = os.popen(f'docker build -t ap1398/hw{xxx} .').read()      #4/4 or 6/6 ...
                # print(ans)
                if( ans.find('Successfully built') != -1):      #it happens when the code can't compile correctly, so the grade of this test is zero
                    # img = os.popen('docker run --rm ap1398/hw1').read() #when the code compile correctlr, we check the result
                    main_img = subprocess.Popen(f'docker run --rm ap1398/hw{xxx}',shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    out, err = main_img.communicate()
                    # print(str(err))
                    img = str(out.decode())         #-------------khoroji mide. ro in bayad donbal failure begardam--------------
                    img_list.append([self.python_testlist[i][1], img])
                    # print(img)
                    if img.find('ERROR:') != -1:
                        final_grade.append([self.python_testlist[i][1],'Error'])           #error
                    elif img.find('FAIL:') == -1:                              #passed
                        final_grade.append([self.python_testlist[i][1], 0])
                    else:
                        ansg = 0
                        numinus = len(re.findall('minus', img)) #get num of failed test(EXPECT_EQ)
                        while numinus > 0:
                            minustr = img[img.rfind("minus"):]
                            minus = re.findall(r'[-+]?\d*\.\d+|\d+', minustr)[0]    #find the grade of each test(EXPECT_EQ)
                            ansg += float(minus)
                            img = img.replace(minustr,'')
                            numinus-=1
                        final_grade.append([self.python_testlist[i][1], ansg/2])              #failed
                else:
                    final_grade.append([self.python_testlist[i][1], 'Error'])               #error
        else:
            for i in range(len(self.python_testlist)-1):
                #change unittest to grade each test
                with open(r'aphw_unittest.py', "r+") as f:
                    data = f.read()
                    f.seek(0)
                    f.write(self.python_testlist[i][0])
                    f.truncate()

                main_img = subprocess.Popen(r'C:/Users/edr/anaconda3/python.exe aphw_unittest.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out, err = main_img.communicate()
                # print(str(err))
                img = str(out.decode())            #khoroji mide. ro in bayad donbal failure begardam 
                img_list.append([self.python_testlist[i][1], img])
                # ans = os.popen('C:/Users/edr/anaconda3/python.exe test.py').read()    #12/12 ...------------------ham adress python ham name test.py bayad avaz shavad--------------------------
                # print(img)
                if( img.find('ERROR:') != -1):      #it happens when the code can't compile correctly, so the grade of this test is zero
                    final_grade.append([self.python_testlist[i][1], 'Error'])               #error
                elif img.find('FAIL:') == -1:                                  #passed
                    final_grade.append([self.python_testlist[i][1], 0])
                else:
                    ansg = 0
                    numinus = len(re.findall('minus', img))                     #get num of failed test(EXPECT_EQ)
                    while numinus > 0:
                        minustr = img[img.rfind("minus"):]
                        minus = re.findall(r'[-+]?\d*\.\d+|\d+', minustr)[0]    #find the grade of each test(EXPECT_EQ)
                        ansg += float(minus)
                        img = img.replace(minustr,'')
                        numinus-=1
                    final_grade.append([self.python_testlist[i][1], ansg/2])           #failed

        with open(r'aphw_unittest.py', "r+") as f:        #change unittest to first manner
                    data = f.read()
                    f.seek(0)
                    f.write(self.python_testlist[-1][0])
                    f.truncate()
        os.chdir(current_path)
        # print(final_grade)
        return final_grade, img_list                            #ex for final grades: [[1,1],[2,0],[3,Compile Error],[4,1]]
                                                                #means test 1 and 4 passed and test 2 failed. test 3 had compile error

    def final_folder_grade(self, folder_grades_list):
        final = 0
        for i in range(len(self.python_each_test_grade)):
            if isinstance(folder_grades_list[i][1], numbers.Number):
                final += self.python_each_test_grade[i][1]-folder_grades_list[i][1]
        return final

    def grading(self):                                          #only python grade
        all_output = []
        final_output = []
        current_path = os.getcwd()
        os.chdir(self.folder_address)
        if not os.path.exists('Python'):
            os.chdir(current_path)
            return False

        os.chdir('Python')
        for subs in os.listdir(os.path.abspath(os.getcwd())):
            if subs[:7] == 'Answer_':
                for manner in os.listdir(os.path.abspath(subs)):
                    f_grade, i_list = self.grade_folder(os.getcwd()+fr'\{subs}\{manner}', False)
                    all_output.append([f_grade, i_list, os.path.abspath(manner)])
        for i in range(len(all_output)):
            if self.final_folder_grade(all_output[i][0]) > self.final_grade:
                self.final_grade = self.final_folder_grade(all_output[i][0])
                final_output = all_output[i]
        self.grades = final_output[0]
        self.images = final_output[1]
        self.best_path = final_output[2]


class student():

    def __init__(self, setting_Data, folder_Address, cpp_testlist, python_testlist, cpp_each_test_grade, python_each_test_grade):
        self.setting_data = setting_Data
        self.folder_address = folder_Address
        self.cpp_testlist = cpp_testlist #vorodi class cppgrade
        self.python_testlist = python_testlist #vorodi class pygrade
        self.cpp_each_test_grade = cpp_each_test_grade #vorodi class cppgrade
        self.python_each_test_grade = python_each_test_grade #vorodi class pygrade
        self.folder_name = os.path.basename(folder_Address)
        self.farsi_name = ''
        self.eng_name = 'None'
        self.student_id = 0  

        self.report_name_format = 0                             #1 if the report name format is okay.
        self.folder_name_format = 0                             #1 if the folder name format is okay.

        self.cpp_grade = cppgrade(setting_Data, folder_Address, cpp_testlist, cpp_each_test_grade)
        # self.grades = []                    #key: number of test, value: point loss of that test. (?!)
        # self.build_okay = 0                 # 1 if built successfully.
        # self.warnings = []                   #key: number of test, value: warning (string)
        # self.images = []                     #key: number of test, value: image (string)
        # self.builds = []
        # self.moss = None
        # self.final_grade = -5
        # self.best_path = folder_Address

    def check_format(self, name):                               #the name must be in shape "MohammadMahdiShojaefar9623065"
        if len(name) < 7 :
            return False
        if ((name[-7:]).isnumeric() and (name[:-7]).isalpha()):
            return name[:-7], name[-7:]
        elif ((name[-8:]).isnumeric() and (name[:-8]).isalpha()):
            return name[:-8], name[-8:]
        return False

    def get_name(self):                                         #path of 'xxxxx_name_assi...sub..._file_' in hw
                                                                #before this func must check the foldar that contain CPlusPlus or Python
        pdfname = []
        subname = []
        temp = []
        os.chdir(self.folder_address)
        s = os.path.basename(self.folder_address)
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

    # def grade(self):
        # self.cpp_grade.run_student()

    def run_student(self):          #zaboonesho check konam age cpp bud self.cpp_grade.grading() run konam age python bud self.py_grade.grading()
        self.pre_process()
        self.cpp_grade.grading()

if __name__ == "__main__":
    print('main ok')
    cpp_testlist = [('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{TEST(APHW1Test, dispFunctionTest)\n{\n  std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    displayDataset(data);\n}}\n', 6), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{TEST(APHW1Test, saveLoadFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::vector<double> w {1, 2, 3, 4, 5, 6, 7};\n    save(w, "wd.csv");\n    std::vector<double> w1;\n    w1 = load("wd.csv");\n    EXPECT_EQ(5, w1[4])<<std::setw(100)<<"***********minus 5***********";\n    EXPECT_EQ(7, w1[6])<<std::setw(100)<<"***********minus 5***********";\n}}\n', 5), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{TEST(APHW1Test, trainFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::vector<double> w (7, 0);\n    w = train(data, w, 0.01, 500, 0.01, false);\n    std::cout<<"Weights...\\n";\n    for(size_t i{}; i<w.size(); std::cout << w[i++] << " ,");\n    std::cout<<"\\n";\n    EXPECT_TRUE((w[0]>5) && (w[0]<6) && (w[6] > 2) && (w[6] < 3))<<std::setw(50)<<"***********minus 20***********";;\n}}\n', 4), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{TEST(APHW1Test, costFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::vector<double> w (7, 1);\n    std::cout << "CostFunction Test here!" << std::endl;\n    EXPECT_TRUE((45 < J(w, data)) && (52 > J(w, data)))<<std::setw(50)<<"***********minus 20***********";;\n}}\n', 3), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{TEST(APHW1Test, gradeFunctionTest)\n{\n    std::vector<double> student{1, 2, 3, 4, 5, 6, 7};\n    std::vector<double> w (7, 1);\n    std::cout << "grade Test here!" << std::endl;\n    EXPECT_EQ(28, grade(w, student))<<std::setw(50)<<"***********minus 20***********";;\n}}\n', 2), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{TEST(APHW1Test, getDataFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::cout << "getData Test here!" << std::endl;\n    EXPECT_EQ(1, data[0][0])<<std::setw(50)<<"***********minus 10***********";;\n    EXPECT_EQ(14.23, data[0][7])<<std::setw(50)<<"***********minus 10***********";;\n}}\n', 1), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{}\n', 0), ('#include <limits.h>\n#include "aphw1.h"\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include "gtest/gtest.h"\nnamespace\n{\nTEST(APHW1Test, getDataFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::cout << "getData Test here!" << std::endl;\n    EXPECT_EQ(1, data[0][0])<<std::setw(50)<<"***********minus 10***********";;\n    EXPECT_EQ(14.23, data[0][7])<<std::setw(50)<<"***********minus 10***********";;\n}\nTEST(APHW1Test, gradeFunctionTest)\n{\n    std::vector<double> student{1, 2, 3, 4, 5, 6, 7};\n    std::vector<double> w (7, 1);\n    std::cout << "grade Test here!" << std::endl;\n    EXPECT_EQ(28, grade(w, student))<<std::setw(50)<<"***********minus 20***********";;\n}\nTEST(APHW1Test, costFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::vector<double> w (7, 1);\n    std::cout <<"CostFunction Test here!" << std::endl;\n    EXPECT_TRUE((45 < J(w, data)) && (52 > J(w, data)))<<std::setw(50)<<"***********minus 20***********";;\n}\nTEST(APHW1Test, trainFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::vector<double> w (7, 0);\n    w = train(data, w, 0.01, 500, 0.01, false);\n    std::cout<<"Weights...\\n";\n    for(size_t i{}; i<w.size(); std::cout << w[i++] << " ,");\n    std::cout<<"\\n";\n    EXPECT_TRUE((w[0]>5) && (w[0]<6) && (w[6] > 2) && (w[6] < 3))<<std::setw(50)<<"***********minus 20***********";;\n}\nTEST(APHW1Test, saveLoadFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    std::vector<double> w {1, 2, 3, 4, 5, 6, 7};\n    save(w, "wd.csv");\n    std::vector<double> w1;\n    w1 = load("wd.csv");\n    EXPECT_EQ(5, w1[4])<<std::setw(100)<<"***********minus 5***********";\n    EXPECT_EQ(7, w1[6])<<std::setw(100)<<"***********minus 5***********";\n}\nTEST(APHW1Test, dispFunctionTest)\n{\n    std::vector<std::vector<double>> data{getData("AP-Data.csv")};\n    displayDataset(data);\n}\n}\n', 0)]
    cpp_each_test_grade = [[6, 0], [5, 10], [4, 20], [3, 20], [2, 20], [1, 20]]
    python_testlist = [('import unittest\nimport aphw6\n\nclass Test(unittest.TestCase):\n    def test2(self):\n        fact = aphw6.Factorial()\n        x = fact(5)\n        self.assertEqual(x, 120, "***********minus 25***********")\n        self.assertEqual(fact.dict[3], 6, "***********minus 20***********")\n\nif __name__==\'__main__\':\n    unittest.main()', 2), ('import unittest\nimport aphw6\n\nclass Test(unittest.TestCase):\n    def test1(self):\n        with open(\'a.jpg\', \'rb\') as file:\n            b1 = file.read()\n        aphw6.code(\'a.jpg\', lambda x: 255 - x)\n        with open(\'a.jpg\', \'rb\') as file:\n            b2 = file.read()\n        self.assertEqual(b1[5], 255-b2[5], "***********minus 55***********")\nif __name__==\'__main__\':\n    unittest.main()', 1), ('import unittest\nimport aphw6\n\nclass Test(unittest.TestCase):\n    def test1(self):\n        with open(\'a.jpg\', \'rb\') as file:\n          b1 = file.read()\n        aphw6.code(\'a.jpg\', lambda x: 255 - x)\n        with open(\'a.jpg\', \'rb\') as file:\n            b2 = file.read()\n        self.assertEqual(b1[5], 255-b2[5], "***********minus 50***********")\n\n    def test2(self):\n        fact = aphw6.Factorial()\n        x = fact(5)\n        self.assertEqual(x, 1210, "***********minus30***********")\n        self.assertEqual(fact.dict[3], 6, "***********minus 20***********")\n\nif __name__==\'__main__\':\n    unittest.main()', 0)]
    python_each_test_grade = [[2,45],[1,55]]
#test pythongrade    
    # x = pygrade(1,r'C:\Users\edr\Desktop\grading\علی یعقوبیان_5482_assignsubmission_file_', python_testlist, python_each_test_grade)
    # x.grading()
    # print('*********************************')
    # print(x.images[0][1])
    # print('*********************************')
    # print(x.images[1][1])
    # print(x.best_path)
    # print(x.final_grade)
    # print(x.grades)
#test cppgrade
    # x = cppgrade(1,r'C:\Users\edr\Desktop\grading\دل ارام غباری_5480_assignsubmission_file_',cpp_testlist,cpp_each_test_grade)
    # x = cppgrade(1,r'C:\Users\edr\Desktop\grading\علی یعقوبیان_5482_assignsubmission_file_',cpp_testlist,cpp_each_test_grade)
    # x.grading()
    # print(x.final_grade)
    # print('')
    # print(x.grades)
    # print('')
    # print(x.warnings)
    # print('')
    # print(x.images[0][1])
    # print('')
    # print(f'build okay = {x.build_okay}')
    # print('')
    # print(x.best_path)
#test student
    # s = student(1,r'C:\Users\edr\Desktop\grading\دل ارام غباری_5480_assignsubmission_file_', cpp_testlist, [], cpp_each_test_grade, [])
    # s.run_student()
    # print(s.report_name_format)
    # print(s.folder_name_format)
    # print(s.farsi_name)
    # print(s.eng_name)
    # print(s.student_id)
    # print('')
    # print(s.cpp_grade.grades)
    # print('')
    # print(s.cpp_grade.warnings)
    # print('')
    # print(s.cpp_grade.images[0][1])
    # print('')
    # print(f'build okay = {s.cpp_grade.build_okay}')
    # print('')
    # print(s.cpp_grade.best_path)
