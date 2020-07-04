import os
import glob
import shutil
import zipfile
import itertools
from pathlib import Path

def create_tree(s, l, makefile_path, googletest_path, dockerfile_path, main_path):
    aphwpath = os.path.abspath(s)                                       #apwh1 path
    hwpath = Path(os.path.abspath(aphwpath)).parent                     #our folder path(named hw)
    Path(str(hwpath) + r'\hw').mkdir(parents = True, exist_ok=True)      #create hw in parent of aphw1
    os.chdir(aphwpath)
    # i=0
    for student in os.listdir(aphwpath):
        Path(str(hwpath) + f'\hw\{student}').mkdir(parents = True, exist_ok=True)   #stu
    aphw_pathlist = os.listdir(aphwpath)        #name of files in aphw1 folder
    for student in aphw_pathlist:
        for ans in os.listdir(student):
            path = os.path.abspath(student)+f'\{ans}' 
            if(zipfile.is_zipfile(path)):
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    Path(str(hwpath) + f'\hw\{student}').mkdir(parents = True, exist_ok=True)#stu
                    zip_ref.extractall(str(hwpath) + f'\hw\{student}\CPlusPlus\{ans[:-4]}')#stu

    os.chdir(str(hwpath)+r'\hw')
    for student in os.listdir(os.path.abspath(os.getcwd())):
        for ans in os.listdir(os.path.abspath(student)):
            create_floder(str(hwpath)+r'\hw'+f'\{student}'+f'\{ans}', l, makefile_path, googletest_path, dockerfile_path, main_path)

def create_floder(s, list_name, makefile_path, googletest_path, dockerfile_path, main_path):
    current_dir = os.path.abspath(os.getcwd())
    os.chdir(s)
    first_folder = os.listdir(os.getcwd())
    first_dir = os.getcwd()
    for sub in os.listdir(s):
        dict = {}
        sub_dir = str(s)+f'\{sub}'
        for name in list_name:
            for root, dirs, files in os.walk(sub_dir):
                for file in files:
                    if file == name:
                        path = os.path.join(root, file)
                        dict.setdefault(name, []).append(path)
        vals = dict.values()
        vals = sorted(vals, key = lambda x:len(x))[::-1]
        answer = []
        for p1,p2 in itertools.product(vals[0],vals[1]):
            answer.append((p1,p2))
        temp = answer.copy()
        for i in range(2,len(vals)):
            answer.clear()
            for p1,p2 in itertools.product(temp,vals[i]):
                answer.append((*p1,p2))
                temp = answer.copy()
        
        for folder in first_folder:
            for i in range(len(answer)):
                path_folder = first_dir + f'\Answer_{folder}' + f'\{folder}_{i+1}'
                Path(path_folder).mkdir(parents=True, exist_ok=True)
                Path(path_folder+r'\cpp').mkdir(parents=True, exist_ok=True)
                Path(path_folder+r'\h').mkdir(parents=True, exist_ok=True)
                for file in answer[i]:
                    shutil.copy(makefile_path, path_folder)
                    shutil.copy(googletest_path, path_folder)
                    shutil.copy(dockerfile_path, path_folder)
                    shutil.copy(main_path, path_folder+r'\cpp')
                    if(str(file)[-4:]=='.cpp'):
                        shutil.copy(file, path_folder+r'\cpp')
                    else:
                        shutil.copy(file, path_folder+r'\h')
    os.chdir(current_dir)           
    

if __name__ == "__main__":
    # l = ['aphw1.cpp','aphw1.h','main.cpp']
    # print(os.getcwd())
    # s = os.getcwd()+'\desktop\zip'
    # create_floder(s,l)
    l = ['aphw1.cpp','aphw1.h','AP-Data.csv']
    makefile_path = r'C:\Users\edr\Desktop\ta\Makefile'
    googletest_path = r'C:\Users\edr\Desktop\ta\aphw1_unittest.cpp'
    dockerfile_path = r'C:\Users\edr\Desktop\ta\Dockerfile'
    main_path = r'C:\Users\edr\Desktop\ta\main.cpp'
    create_tree(r'C:\Users\edr\desktop\grading\APHW', l, makefile_path, googletest_path, dockerfile_path, main_path)
    # print(os.getcwd())
    # shutil.rmtree(os.getcwd(), ignore_errors = True)
    # l1 = ['a','b','c']
    # l2 = [3,5,]
    # l3 = ['+']
    # create_floder(l1,l1,l2,l3)


# if(not zipfile.is_zipfile(path)):
                # os.remove(path)
                # shutil.rmtree(path, ignore_errors = True)


# dataset ro jay dorost gharar bedam(.csv)
#agar yek ya do ta faghat file list mojod boud ye fekri bokonam---ye if bezaram sizesh 0 nabashe error bede
