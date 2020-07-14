import re
import os

def comment(s):
    os.chdir(s)                                             #path of grading folder
    s = open("aphw1_unittest.cpp").read()
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
    print(s)
    #at last we have: testlist = [(test num n, n), (test num n-1, n-1),...(test num 1, 1), (empty namespace, 0), (full test, 0)]
    return test_list

def grade(s, test_list):                                    #s is the path of grading folder
    current_path = os.path.abspath(os.getcwd())
    final_grade = []
    os.chdir(s)                                             #first we create test list, then we grade the code

    #open unittest and clear all tests
    with open(r'cpp\aphw1_unittest.cpp', "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(test_list[-2][0])
        f.truncate()

    stop = os.popen('docker stop hw1').read()
    ans = os.popen('docker build -t ap1398/hw1 .').read()   #12/12 ...check the code is ok or not


    if( ans.find('Successfully built') == -1):              #it happens when the code cant compile correctly, so the final grade is zero
        final_grade = [[i+1,'Compile Error All'] for i in range(len(test_list)-1)]
    else:                                                   #now we grade each test
        for i in range(len(test_list)-2):
            #change unittest to grade each test
            with open(r'cpp\aphw1_unittest.cpp', "r+") as f:
                data = f.read()
                f.seek(0)
                f.write(test_list[i][0])
                f.truncate()

            stop = os.popen('docker stop hw1').read()
            ans = os.popen('docker build -t ap1398/hw1 .').read()   #12/12 ...
            if( ans.find('Successfully built') != -1):      #it happens when the code can't compile correctly, so the grade of this test is zero
                img = os.popen('docker run --rm ap1398/hw1').read() #when the code compile correctlr, we check the result
                if img.find('<<<SUCCESS>>>') != -1:         #passed
                    final_grade.append([test_list[i][1],1])
                else:
                    final_grade.append([test_list[i][1],0]) #failed
            else:
                final_grade.append([test_list[i][1],'Compile Error'])   #copmile error

    os.chdir(current_path)
    return final_grade                                      #ex for final grades: [[1,1],[2,0],[3,Compile Error],[4,1]]
                                                            #means test 1 and 4 passed and test 2 failed. test 3 had compile error
