import re
import os

def comment(s):
    os.chdir(s)
    # print(os.getcwd())
    s = open("aphw1_unittest.cpp").read()
    namespace = s[s.find("namespace\n{")+11:s.rfind("}")]
    # print(namespace)
    temp = namespace
    s_tests = s.replace(namespace, '')
    # print(s_tests)
    
    test_list = []
    while temp.find("TEST(") != -1:
        test = temp[temp.rfind("TEST("):temp.rfind("}")+1]
        temp = temp.replace(test,'')
        full_test = s.replace(namespace, test)
        test_list.append(full_test)

    for i in range(len(test_list)):
        test_list[i] = (test_list[i], len(test_list)-i)
    
    test_list.append((s_tests,0))

    return test_list


#--DEBUGGING--
# def grade(s, test_list):
#     os.chdir(s)
#     print(s)
#     os.system('docker stop hw1')
#     ans = os.popen('docker build -t ap1398/hw1 .').read()   ##12/12 ...
#     write = open('aphw1_unittest.cpp','w')
#     write.write(test_list[-1][0])

#     if( ans.find('returned a non-zero code')):
#         print('Erorrrr')
#     else:
#         img = os.popen('docker run --rm ap1398/hw1').read()     ##khoroji ./main docker


if __name__ == "__main__":
    # os.chdir('desktop\cplusplus\Answer_MohammadMahdiShojaefar9623065\MohammadMahdiShojaefar9623065_1')
    os.chdir('MohammadMahdiShojaefar9623065_1')
    s = os.getcwd()
    # os.chdir('MohammadMahdiShojaefar9623065_1')
    # x = os.getcwd()
    # print(s[])
    ans = comment(s+r'\cpp')
    # print(ans[4])
    grade(s, ans)
