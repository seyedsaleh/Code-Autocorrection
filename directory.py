import os
import glob
import shutil
import zipfile
import itertools
from pathlib import Path

#import setting.py

class directory():    

    def __init__(self, setting_data, aphwfolderpath, cppfolder, pythonfolder):
        self.setting_data = setting_data
        self.cppfolder = cppfolder
        self.pythonfolder = pythonfolder
        self.aphwfolderpath = aphwfolderpath

    def create_tree(self, s, l, cppfolder, pythonfolder):                         #l is a list consist of name of files
        ispython = False
        iscpp = False
        pythonfilelist = []
        cppfilelist = []
        for filename in l:                                                  #determine the language of answers
            if filename[-3:]=='.py':
                ispython = True
                pythonfilelist.append(filename)
            if filename[-2:]=='.h' or filename[-4:]=='.hpp' or filename[-4:]=='.cpp':
                iscpp = True
                cppfilelist.append(filename)
        aphwpath = os.path.abspath(s)                                       #apwh_i path
        hwpath = Path(os.path.abspath(aphwpath)).parent                     #our folder path(named hw)
        Path(str(hwpath) + r'\hw').mkdir(parents = True, exist_ok=True)     #create hw in parent of aphw1
        os.chdir(aphwpath)
        for student in os.listdir(aphwpath):
            Path(str(hwpath) + f'\hw\{student}').mkdir(parents = True, exist_ok=True)
        aphw_pathlist = os.listdir(aphwpath)                                 #list of files in aphw1 folder ()
        for student in aphw_pathlist:
            for ans in os.listdir(student):
                path = os.path.abspath(student)+f'\{ans}' 
                if(zipfile.is_zipfile(path)):                               #check the file is zip or not(rar or anything else) 
                                                                            #if there isn't any zip file, the grade will be zero
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        Path(str(hwpath) + f'\hw\{student}').mkdir(parents = True, exist_ok=True)
                        if iscpp:
                            zip_ref.extractall(str(hwpath) + f'\hw\{student}\CPlusPlus\{ans[:-4]}')     #unzip file in CPlusPlus folder
                                                                            #ans[:-4] show the name of sub without the '.zip'
                        if ispython:
                            zip_ref.extractall(str(hwpath) + f'\hw\{student}\Python\{ans[:-4]}')        #unzip file in Python folder
                                                                            #ans[:-4] show the name of sub without the '.zip'
        #now we change dir to 'hw' to create folders to grade easier
        os.chdir(str(hwpath)+r'\hw')
        for student in os.listdir(os.path.abspath(os.getcwd())):            #name of students are same as the name of students in aphw_i folder
            for ans in os.listdir(os.path.abspath(student)):                #CPlusPlus or Python
                if ans == 'CPlusPlus':
                    self.create_floder(str(hwpath)+r'\hw'+f'\{student}'+f'\{ans}', 'cpp', cppfilelist, self.cppfolder)
                if ans == 'Python':
                    self.create_floder(str(hwpath)+r'\hw'+f'\{student}'+f'\{ans}', 'python', pythonfilelist, self.pythonfolder)

    def create_floder(self, s, lan, list_name, folder_path):
        current_dir = os.path.abspath(os.getcwd())                          #the path that we come from to this function
        os.chdir(s)                                                         #hw\sub\CPlsPlus or Python
        first_folder = os.listdir(os.getcwd())                              #list of folder in CPlusPlus, actually the subs are in this folder
        first_dir = os.getcwd()
        for sub in os.listdir(s):                                           #sub is submission
            dict = {}                                                       #for ex: dict = {'aphw1.cpp' : [path1, path2, path3]}
            sub_dir = str(s)+f'\{sub}'
            for name in list_name:                                          #now search each file(for ex: aphw1.cpp) in sub folder
                for root, dirs, files in os.walk(sub_dir):
                    for file in files:
                        if file == name:
                            path = os.path.join(root, file)
                            dict.setdefault(name, []).append(path)
            vals = list(dict.values())
            vals = self.check(vals)
            vals = sorted(vals, key = lambda x:len(x))[::-1]                #sort dict according to the paths list
            answer = []                                                     #answer is a list of jaygasht ha! :))
                                                                            #ex for final result: [[aphw1.cpp path1, aphw1.h path1]
                                                                            #                      [aphw1.cpp path1, aphw1.h path2]]
            if len(list(dict.keys())) == 1 :
                answer = list(map(lambda el:[el], list(dict.values())[0]))

            #calculate all state
            if len(list(dict.keys())) > 1 :
                for p1,p2 in itertools.product(vals[0],vals[1]):
                    answer.append((p1,p2))
            temp = answer.copy()
            for i in range(2,len(vals)):
                answer.clear()
                for p1,p2 in itertools.product(temp,vals[i]):
                    answer.append((*p1,p2))
                    temp = answer.copy()
            
            #create some folders for grading easier
            if lan == 'cpp':
                for i in range(len(answer)):
                    path_folder = first_dir + f'\Answer_{sub}' + f'\{sub}_{i+1}'#folder
                    Path(path_folder).mkdir(parents=True, exist_ok=True)
                    Path(path_folder+r'\cpp').mkdir(parents=True, exist_ok=True)
                    Path(path_folder+r'\h').mkdir(parents=True, exist_ok=True)
                    for file in answer[i]:
                        for dataset in os.listdir(folder_path+'\dataset'):
                            shutil.copy(folder_path + '\dataset' + f'\{dataset}', path_folder)
                        shutil.copy(folder_path + r'\Makefile', path_folder)    #find and copy other files
                        shutil.copy(folder_path + r'\Dockerfile', path_folder)
                        shutil.copy(folder_path + r'\aphw_unittest.cpp', path_folder+r'\cpp')
                        shutil.copy(folder_path + r'\main.cpp', path_folder+r'\cpp')
                        if(str(file)[-4:]=='.cpp' or str(file)[-4:]=='.hpp'):
                            shutil.copy(file, path_folder+r'\cpp')
                        elif str(file)[-2:]=='.h':
                            shutil.copy(file, path_folder+r'\h')
            if lan == 'python':
                for i in range(len(answer)):
                    path_folder = first_dir + f'\Answer_{sub}' + f'\{sub}_{i+1}'#folder
                    Path(path_folder).mkdir(parents=True, exist_ok=True)
                    for file in answer[i]:
                        for dataset in os.listdir(folder_path+'\dataset'):
                            shutil.copy(folder_path + '\dataset' + f'\{dataset}', path_folder)
                        shutil.copy(folder_path + r'\Makefile', path_folder)    #find and copy other files
                        shutil.copy(folder_path + r'\Dockerfile', path_folder)
                        shutil.copy(folder_path + r'\aphw_unittest.py', path_folder)
                        shutil.copy(folder_path + r'\requirements.txt', path_folder)
                        shutil.copy(file, path_folder)
        os.chdir(current_dir)           

    def check(self, vals):                                                        #get a list and convert the list to unique-list
        current_path = os.path.abspath(os.getcwd())
        output = []
        #finding same files
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

    def start(self):
        aphwzippath = os.path.abspath(self.aphwfolderpath)
        aphwpath = Path(str(Path(os.path.abspath(aphwzippath)).parent) + r'\aphw')
        hwpath = Path(str(Path(os.path.abspath(aphwzippath)).parent) + r'\hw')
        if os.path.exists(hwpath):
            print('pls remove or rename hw folder')
            return False
        elif os.path.exists(aphwpath):
            print('pls remove or rename aphw folder')
            return False
        else:
            with zipfile.ZipFile(self.aphwfolderpath, 'r') as zip_ref:
                Path(aphwpath).mkdir(parents = True, exist_ok=True)
                zip_ref.extractall(aphwpath)
                self.create_tree(aphwpath, self.setting_data.file_names, self.cppfolder, self.pythonfolder)
                shutil.rmtree(aphwpath)
            return True

    def pycomment(self, unittestpath):
        os.chdir(unittestpath)                                             #path of grading folder
        s = open("aphw_unittest.py").read()
        test_class = s[s.find("class Test(unittest.TestCase):")+30:s.rfind("if __name__=='__main__':")]   #all test
        temp = test_class
        test_list = []                                          #list of tuple(num of test, unittest)
        while temp.find("def") != -1:
            temp1 = temp[:temp.rfind("def")]
            test = temp[temp1.rfind("\n"):]                     #find last test that start from last endline before it
            temp = temp.replace(test,'')                        #clear last test
            full_test = s.replace(test_class, test)             #create a code with only one test(there is a test in test class)
            test_list.append(full_test)    
        #there are some code in test_list without the num of test, now we determine num of them
        for i in range(len(test_list)):
            test_list[i] = (test_list[i], len(test_list)-i)

        test_list.append((s,0))                                 #the orginal unittest
        #at last we have: testlist = [(test num n, n), (test num n-1, n-1),...(test num 1, 1), (full test, 0)]
        return test_list

    def cppcomment(self, unittestpath):
        os.chdir(unittestpath)                                  #path of grading folder
        s = open("aphw_unittest.cpp").read()
        namespace = s[s.find("namespace\n{")+11:s.rfind("}")]   #all test
        temp = namespace
        s_tests = s.replace(namespace, '')                      #clear all test
        
        test_list = []                                          #list of tuple(num of test, unittest)
        while temp.find("TEST(") != -1:
            test = temp[temp.rfind("TEST("):temp.rfind("}")+1]  #find last test
            temp = temp.replace(test,'')                        #clear last test
            full_test = s.replace(namespace, test)              #create a code with only one test(there is a test in namespace)
            test_list.append(full_test)                         
        #there are some code in test_list without the num of test, now we determine num of them
        for i in range(len(test_list)):
            test_list[i] = (test_list[i], len(test_list)-i)
        
        test_list.append((s_tests,0))
        test_list.append((s,0))                                 #the orginal unittest
        #at last we have: testlist = [(test num n, n), (test num n-1, n-1),...(test num 1, 1), (empty namespace, 0), (full test, 0)]
        return test_list

