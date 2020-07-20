import os
import glob
import shutil
import zipfile
import itertools
from pathlib import Path

def create_tree(s, l, cppfolder, pythonfolder):                         #l is a list consist of name of files
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
                create_floder(str(hwpath)+r'\hw'+f'\{student}'+f'\{ans}', 'cpp', cppfilelist, cppfolder)
            if ans == 'Python':
                create_floder(str(hwpath)+r'\hw'+f'\{student}'+f'\{ans}', 'python', pythonfilelist, pythonfolder)

def create_floder(s, lan, list_name, folder_path):
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
        vals = check(vals)
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
        
        #for each sub in first_folder:
        #create some folders for grading easier
        if lan == 'cpp':
            for i in range(len(answer)):
                path_folder = first_dir + f'\Answer_{sub}' + f'\{sub}_{i+1}'#folder
                Path(path_folder).mkdir(parents=True, exist_ok=True)
                Path(path_folder+r'\cpp').mkdir(parents=True, exist_ok=True)
                Path(path_folder+r'\h').mkdir(parents=True, exist_ok=True)
                for file in answer[i]:
                    # makefile_path, googletest_path, dockerfile_path
                    for dataset in os.listdir(folder_path):
                        if dataset[-4:] == '.csv':                          #find and copy dataset files
                            shutil.copy(folder_path + f'\{dataset}', path_folder)
                    shutil.copy(folder_path + r'\Makefile', path_folder)    #find and copy other files
                    shutil.copy(folder_path + r'\Dockerfile', path_folder)
                    shutil.copy(folder_path + r'\aphw1_unittest.cpp', path_folder+r'\cpp')
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
                    # makefile_path, googletest_path, dockerfile_path
                    for dataset in os.listdir(folder_path):
                        if dataset[-4:] == '.csv':                          #find and copy dataset files
                            shutil.copy(folder_path + f'\{dataset}', path_folder)
                    shutil.copy(folder_path + r'\Makefile', path_folder)    #find and copy other files
                    shutil.copy(folder_path + r'\Dockerfile', path_folder)
                    shutil.copy(folder_path + r'\aphw1_unittest.cpp', path_folder)
                    shutil.copy(folder_path + r'\requirements.txt', path_folder)
                    shutil.copy(file, path_folder)
    os.chdir(current_dir)           
    
def check(vals):                                        #get a list and convert the list to unique-list
    current_path = os.path.abspath(os.getcwd())
    # print(vals)
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
    # print(output)
    os.chdir(current_path)
    return output

if __name__ == "__main__":
    l = ['aphw1.cpp','aphw1.h']
    folder = r'C:\Users\edr\Desktop\ta'
    folder2 = r'C:\Users\edr\Desktop\ta1'
    create_tree(r'C:\Users\edr\desktop\grading\APHW1', l, folder, folder2)
