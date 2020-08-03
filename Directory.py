import os
import glob
import shutil
import zipfile
import itertools
from pathlib import Path
from PyQt5 import QtCore


class Directory(QtCore.QThread):
    display_signal = QtCore.pyqtSignal([str, bool])

    def __init__(self, window, setting_data, aphwfolderpath, cppfolder, pythonfolder):
        QtCore.QThread.__init__(self, parent=window)
        self.setting_data = setting_data
        self.cppfolder = cppfolder
        self.pythonfolder = pythonfolder
        self.aphwfolderpath = aphwfolderpath

    def create_tree(self, s, l, cppfolder, pythonfolder):  # l is a list consist of name of files
        ispython = False
        iscpp = False
        pythonfilelist = []
        cppfilelist = []
        for filename in l:  # determine the language of answers
            if filename[-3:] == '.py':
                ispython = True
                pythonfilelist.append(filename)
            if filename[-2:] == '.h' or filename[-4:] == '.hpp' or filename[-4:] == '.cpp':
                iscpp = True
                cppfilelist.append(filename)
        self.display_signal.emit("در حال تلاش برای آن زیپ کردن فایل ها", True, False)
        aphwpath = os.path.abspath(s)  # apwh_i path
        hwpath = Path(os.path.abspath(aphwpath)).parent  # our folder path(named hw)
        Path(str(hwpath) + r'\hw').mkdir(parents=True, exist_ok=True)  # create hw in parent of aphw_i
        os.chdir(aphwpath)
        for student in os.listdir(aphwpath):
            Path(str(hwpath) + fr'\hw\{student}').mkdir(parents=True, exist_ok=True)
        aphw_pathlist = os.listdir(aphwpath)  # list of files in aphw_i folder ()
        for student in aphw_pathlist:
            for ans in os.listdir(student):
                path = os.path.abspath(student) + fr'\{ans}'
                if (zipfile.is_zipfile(path)):  # check the file is zip or not(rar or anything else)
                                                # if there isn't any zip file, the grade will be zero
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        Path(str(hwpath) + fr'\hw\{student}').mkdir(parents=True, exist_ok=True)
                        if iscpp:
                            try:
                                zip_ref.extractall(
                                    str(hwpath) + fr'\hw\{student}\CPlusPlus\{ans[:-4]}')  # unzip file in CPlusPlus folder
                                #                                                            ans[:-4] show the name of sub without the '.zip'
                            except:
                                self.display_signal.emit(f"{path} ان زیپ نشد.", False, False)
                            
                        if ispython:
                            try:
                                zip_ref.extractall(
                                    str(hwpath) + fr'\hw\{student}\Python\{ans[:-4]}')  # unzip file in Python folder
                                #                                                         ans[:-4] show the name of sub without the '.zip'
                            except:
                                self.display_signal.emit(f"{path} ان زیپ نشد.", False, False)
        # now we change dir to 'hw' to create folders to grade easier
        self.display_signal.emit("همه ارسال ها ان زیپ شدند.", True, False)
        self.display_signal.emit("در حال تلاش برای محاسبه تمام حالات و ساخت پوشه های موردنظر.", True, False)
        os.chdir(str(hwpath) + r'\hw')
        for student in os.listdir(
                os.path.abspath(os.getcwd())):  # name of students are same as the name of students in aphw_i folder
            for ans in os.listdir(os.path.abspath(student)):  # CPlusPlus or Python
                if ans == 'CPlusPlus':
                    self.create_floder(str(hwpath) + r'\hw' + fr'\{student}' + fr'\{ans}', 'cpp', cppfilelist, cppfolder)
                if ans == 'Python':
                    self.create_floder(str(hwpath) + r'\hw' + fr'\{student}' + fr'\{ans}', 'python', pythonfilelist,
                                       pythonfolder)

    def create_floder(self, s, lan, list_name, folder_path):
        current_dir = os.path.abspath(os.getcwd())  # the path that we come from to this function
        os.chdir(s)  # hw\sub\CPlsPlus or Python
        # first_folder = os.listdir(os.getcwd())  # list of folder in CPlusPlus, actually the subs are in this folder
        first_dir = os.getcwd()
        for sub in os.listdir(s):  # sub is submission
            dic = {}  # for ex: dic = {'aphw1.cpp' : [path1, path2, path3]}
            sub_dir = str(s) + fr'\{sub}'
            for name in list_name:  # now search each file(for ex: aphw1.cpp) in sub folder
                for root, dirs, files in os.walk(sub_dir):
                    for file in files:
                        if file == name:
                            path = os.path.join(root, file)
                            dic.setdefault(name, []).append(path)
            vals = list(dic.values())
            vals = self.check(vals)
            vals = sorted(vals, key = lambda x: len(x))[::-1]  # sort dictionary according to the paths list
            answer = []  # answer is a list of jaygasht ha! :))
            # ex for final result: [[aphw1.cpp path1, aphw1.h path1]
            #                      [aphw1.cpp path1, aphw1.h path2]]
            if len(list(dic.keys())) == 1:
                answer = list(map(lambda el: [el], list(dic.values())[0]))

            # calculate all state
            if len(list(dic.keys())) > 1:
                for p1, p2 in itertools.product(vals[0], vals[1]):
                    answer.append((p1, p2))
            temp = answer.copy()
            for i in range(2, len(vals)):
                answer.clear()
                for p1, p2 in itertools.product(temp, vals[i]):
                    answer.append((*p1, p2))
                    temp = answer.copy()

            # create some folders for grading easier
            if lan == 'cpp':
                for i in range(len(answer)):
                    path_folder = first_dir + fr'\Answer_{sub}' + fr'\{sub}_{i + 1}'  # folder
                    Path(path_folder).mkdir(parents=True, exist_ok=True)
                    Path(path_folder + r'\cpp').mkdir(parents=True, exist_ok=True)
                    Path(path_folder + r'\h').mkdir(parents=True, exist_ok=True)
                    for file in answer[i]:
                        for dataset in os.listdir(folder_path + r'\dataset'):
                            shutil.copy(folder_path + r'\dataset' + fr'\{dataset}', path_folder)
                        shutil.copy(folder_path + r'\Makefile', path_folder)  # find and copy other files
                        shutil.copy(folder_path + r'\Dockerfile', path_folder)
                        shutil.copy(folder_path + r'\aphw_unittest.cpp', path_folder + r'\cpp')
                        shutil.copy(folder_path + r'\main.cpp', path_folder + r'\cpp')
                        if (str(file)[-4:] == '.cpp' or str(file)[-4:] == '.hpp'):
                            shutil.copy(file, path_folder + r'\cpp')
                        elif str(file)[-2:] == '.h':
                            shutil.copy(file, path_folder + r'\h')
            if lan == 'python':
                for i in range(len(answer)):
                    path_folder = first_dir + fr'\Answer_{sub}' + fr'\{sub}_{i + 1}'  # folder
                    Path(path_folder).mkdir(parents=True, exist_ok=True)
                    for file in answer[i]:
                        for dataset in os.listdir(folder_path + r'\dataset'):
                            shutil.copy(folder_path + r'\dataset' + fr'\{dataset}', path_folder)
                        shutil.copy(folder_path + r'\Makefile', path_folder)  # find and copy other files
                        shutil.copy(folder_path + r'\Dockerfile', path_folder)
                        shutil.copy(folder_path + r'\aphw_unittest.py', path_folder)
                        shutil.copy(folder_path + r'\requirements.txt', path_folder)
                        shutil.copy(file, path_folder)
        os.chdir(current_dir)

    def check(self, vals):  # get a list and convert the list to unique-list
        current_path = os.path.abspath(os.getcwd())
        output = []
        # finding same files
        for li in vals:
            temp = []
            tempcode = []
            licode = []
            for path in li:
                with open(path, 'r') as reader:
                    code = reader.read()
                licode.append(code)
            for i in range(len(li)):
                if licode[i] not in tempcode:
                    tempcode.append(licode[i])
                    temp.append(li[i])
            output.append(temp)
        os.chdir(current_path)
        return output

    def run(self):
        aphwzippath = os.path.abspath(self.aphwfolderpath)
        aphwpath = Path(str(Path(os.path.abspath(aphwzippath)).parent) + r'\aphw')
        hwpath = Path(str(Path(os.path.abspath(aphwzippath)).parent) + r'\hw')
        if aphwzippath == '':
            self.display_signal.emit("فایل تمرین دانشجویان را وارد کنید.", False, True)                    
        
        if not zipfile.is_zipfile(aphwzippath):
            self.display_signal.emit("فایل تمرین دانشجویان باید حتما زیپ باشد", False, True)

        if self.setting_data.file_names == []:
            self.display_signal.emit("نام فایل های کد این تمرین را وارد کنید.", False, True)  

        for files in self.setting_data.file_names:
            if files[-3:] == '.py':
                if self.pythonfolder == '':
                    self.display_signal.emit("پوشه تصحیح Python را وارد کنید.", False, True)
                if not os.path.isfile(str(self.pythonfolder) + r'\Makefile'):
                    self.display_signal.emit("Makefile باید در پوشه تصحیح Python باشد.", False, True)
                if not os.path.isfile(str(self.pythonfolder) + r'\requirements.txt'):
                    self.display_signal.emit("requirements.txt باید در پوشه تصحیح Python باشد.", False, True)
                if not os.path.isfile(str(self.pythonfolder) + r'\Dockerfile'):
                    self.display_signal.emit("Dockerfile باید در پوشه تصحیح Python باشد.", False, True)
                if not os.path.isfile(str(self.pythonfolder) + r'\aphw_unittest.py'):
                    self.display_signal.emit("aphw_unittest.py باید در پوشه تصحیح Python باشد.", False, True)
                if not os.path.isdir(str(self.pythonfolder) + r'\dataset'):
                    self.display_signal.emit("پوشه dataset باید در پوشه تصحیح Python باشد.", False, True)

            if files[-4:] == '.cpp' or files[-4:] == '.hpp' and files[-2:] == '.h':
                if self.cppfolder == '':
                    self.display_signal.emit("پوشه تصحیح C++ را وارد کنید.", False, True)   
                if not os.path.isfile(str(self.cppfolder) + r'\Makefile'):
                    self.display_signal.emit("Makefile باید در پوشه تصحیح C++ باشد.", False, True)
                if not os.path.isfile(str(self.cppfolder) + r'\main.cpp'):
                    self.display_signal.emit("main.cpp باید در پوه تصحیح C++ باشد", False, True)
                if not os.path.isfile(str(self.cppfolder) + r'\Dockerfile'):
                    self.display_signal.emit("Dockerfile باید در پوشه تصحیح C++ باشد.", False, True)
                if not os.path.isfile(str(self.cppfolder) + r'\aphw_unittest.cpp'):
                    self.display_signal.emit("aphw_unittest.cpp باید در پوشه تصحیح C++ باشد.", False, True)
                if not os.path.isdir(str(self.cppfolder) + r'\dataset'):
                    self.display_signal.emit("پوشه dataset باید در پوشه تصحیح C++ باشد.", False, True)

        if os.path.exists(hwpath):
            self.display_signal.emit("نباید پوشه ای با نام hw در کنار فایل زیپ تمرین دانشجویان باشد.", False, True)
        elif os.path.exists(aphwpath):
            self.display_signal.emit("نباید پوشه ای با نام aphw در کنار فایل زیپ تمرین دانشجویان باشد.", False, True)
        else:
            with zipfile.ZipFile(self.aphwfolderpath, 'r') as zip_ref:
                Path(aphwpath).mkdir(parents=True, exist_ok=True)
                zip_ref.extractall(aphwpath)
                for files in os.listdir(aphwpath):
                    if not os.path.isdir(str(aphwpath) + fr'\{files}'):
                        self.display_signal.emit("فایل تمرین دانشجویان فقط باید حاوی تعدادی فولدر باشد.", False, True)

                self.create_tree(aphwpath, self.setting_data.file_names, self.cppfolder, self.pythonfolder)
                shutil.rmtree(aphwpath)
            self.display_signal.emit("تمام حالت ها ساخته شد.", True, True)  #finished directory run

    def pycomment(self):
        os.chdir(self.pythonfolder)  # path of grading folder
        s = open("aphw_unittest.py").read()
        if s.find("class Test(unittest.TestCase):") == -1:
            self.display_signal.emit("لطفا فایل aphw_unittest.py را بازنویسی کنید و دوباره برنامه را ران بگیرید.", False, True)

        test_class = s[s.find("class Test(unittest.TestCase):") + 30:s.rfind("if __name__=='__main__':")]  # all test
        temp = test_class
        test_list = []  # list of tuple(num of test, unittest)
        while temp.find("def") != -1:
            temp1 = temp[:temp.rfind("def")]
            test = temp[temp1.rfind("\n"):]  # find last test that start from last endline before it
            temp = temp.replace(test, '')  # clear last test
            full_test = s.replace(test_class, test)  # create a code with only one test(there is a test in test class)
            test_list.append(full_test)
        # there are some code in test_list without the num of test, now we determine num of them
        for i in range(len(test_list)):
            test_list[i] = (test_list[i], len(test_list) - i)

        test_list.append((s, 0))  # the orginal unittest
        # at last we have: testlist = [(test num n, n), (test num n-1, n-1),...(test num 1, 1), (full test, 0)]
        return test_list

    def cppcomment(self):
        os.chdir(self.cppfolder)  # path of grading folder
        s = open("aphw_unittest.cpp").read()
        if s.find("namespace\n{") == -1:
            self.display_signal.emit("لطفا فایل aphw_unittest.cpp را بازنویسی کنید و دوباره برنامه را ران بگیرید. ", False, True)
        
        namespace = s[s.find("namespace\n{") + 11:s.rfind("}")]  # all test
        temp = namespace
        s_tests = s.replace(namespace, '')  # clear all test

        test_list = []  # list of tuple(num of test, unittest)
        while temp.find("TEST(") != -1:
            test = temp[temp.rfind("TEST("):temp.rfind("}") + 1]  # find last test
            temp = temp.replace(test, '')  # clear last test
            full_test = s.replace(namespace, test)  # create a code with only one test(there is a test in namespace)
            test_list.append(full_test)
        # there are some code in test_list without the num of test, now we determine num of them
        for i in range(len(test_list)):
            test_list[i] = (test_list[i], len(test_list) - i)

        test_list.append((s_tests, 0))
        test_list.append((s, 0))  # the orginal unittest
        # at last we have: testlist = [(test num n, n), (test num n-1, n-1),...(test num 1, 1), (empty namespace, 0), (full test, 0)]
        return test_list
    
    def cpp_eachtest_grade(self):
        eachtest_grade = []
        test_list = self.cppcomment(self.cppfolder+r'\aphw_unittest.cpp')
        for i in range(len(test_list)-2):
            ansg = 0
            numinus = len(re.findall(self.setting_data.minus_keyWord, test_list[i][0]))
            s = test_list[i][0]
            while numinus > 0:
                minustr = s[s.rfind(self.setting_data.minus_keyWord):]
                minus = re.findall(r'[-+]?\d*\.\d+|\d+', minustr)[0]    #find the grade of each test(EXPECT_EQ)
                ansg += float(minus)
                s = s.replace(minustr,'')
                numinus-=1
            eachtest_grade.append([test_list[i][1], ansg])
        return eachtest_grade

    def python_eachtest_grade(self):
        eachtest_grade = []
        test_list = self.pycomment(self.pythonfolder+r'\aphw_unittest.py')
        for i in range(len(test_list)-1):
            ansg = 0
            numinus = len(re.findall(self.setting_data.minus_keyWord, test_list[i][0]))
            s = test_list[i][0]
            while numinus > 0:
                minustr = s[s.rfind(self.setting_data.minus_keyWord):]
                minus = re.findall(r'[-+]?\d*\.\d+|\d+', minustr)[0]    #find the grade of each test(assert_equal)
                ansg += float(minus)
                s = s.replace(minustr,'')
                numinus-=1
            eachtest_grade.append([test_list[i][1], ansg])
        return eachtest_grade

    def create_test(self):
        aphwzippath = os.path.abspath(self.aphwfolderpath)
        testpath = Path(str(Path(os.path.abspath(aphwzippath)).parent) + r'\test')
        Path(testpath).mkdir(parents=True, exist_ok=True)
        shutil.copytree(self.cppfolder, testpath)
        shutil.copytree(self.pythonfolder, testpath)

    def view(self, s):
        current = os.getcwd()

        aphwunzipedpath = os.path.abspath(s)
        viewpath = Path(str(Path(os.path.abspath(aphwunzipedpath)).parent) + r'\s_hw')
        Path(viewpath).mkdir(parents=True, exist_ok=True)
        os.chdir(aphwunzipedpath)
        for student in os.listdir(aphwunzipedpath):
            for ans in os.listdir(student):
                path = os.path.abspath(student) + fr'\{ans}'
                if (zipfile.is_zipfile(path)):  # check the file is zip or not(rar or anything else)
                                                # if there isn't any zip file, the grade will be zero
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        foldername = ''
                        for ch in student:
                            if not(ch>='a' and ch<='z') and not(ch>='A' and ch<='Z') and not(ch>='0' and ch<='9') and ch != '_':
                                foldername += ch
                        Path(str(viewpath) + fr'\{foldername}').mkdir(parents=True, exist_ok=True)
                        try:
                            zip_ref.extractall(
                                str(viewpath) + fr'\{foldername}\{ans[:-4]}')  # unzip file in CPlusPlus folder
                                                                            # ans[:-4] show the name of sub without the '.zip'
                        except:
                            print(f"{path} ان زیپ نشد.")
        os.chdir(current)


