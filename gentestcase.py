# -*- coding:utf-8 -*-  
'''
生成集成测试用例
'''
import sys,csv

def read_case(filename):
    s=""
    path = 'case\\{}.txt'.format(filename.strip())
    with open(path,'r') as f:
        for _ in f:
            s+=_
    return s

def read_step(filename):
    s=""
    path = 'step\\{}.txt'.format(filename.strip())
    with open(path,'r') as f:
        for _ in f:
            s+=_
    return s

def read_except(filename):
    s=""
    for x in filename.split('|'):
        path = 'except\\{}.txt'.format(x.strip())
        if len(s) > 0:
            s+='\n'
        with open(path,'r') as f:
            for _ in f:
                s+=_
    return s

            
def parse_testcase_describe(filename):
    ret=[]
    with open(filename+'.txt', 'r') as f:
        for l in f:
            if '#' == l[0]:
                continue
            (case,step,out_except) = l.split('，')
            print(case,step,out_except)
            l1 = read_case(case)
            l2 = read_step(step)
            l3 = read_except(out_except)
            endcase = True
            for n,x in enumerate(l2.split('\n')):
                if endcase:
                    if '\t' != x[0]:
                        if n == 0:
                            ret.append((l1,x,'',l3))
                        else:
                            ret.append(('',x,'',l3))
                    else:
                        ret.append(('','',x,l3))
                    endcase = False
                    continue
                if len(x.strip()) == 0:
                    endcase = True
                    continue
                (a,b,c,d) = ret.pop(-1)
                if len(c) == 0:
                    c = x
                    ret.append((a,b,c,d))
                else:
                    ret.append((a,b,c,d))
                    ret.append(('','',x,''))
    return ret
        

def read_testcase_def(allcases):
    with open('testcase_def.txt', 'r') as f:
        for l in f:
            #注释不管
            if '#' != l[0]:
                allcases.append(l)


if __name__ == '__main__':
    allcases=[]
    read_testcase_def(allcases)
    if len(allcases) < 0:
        print('用例定义文件为空，程序退出')
        sys.exit()
    print('生成如下用例:')
    with open('test.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for l in allcases:
            print(l)
            count = 0
            onesense = parse_testcase_describe(l.strip())      
            for x in onesense:
                caseid=''
                (a,b,c,d) = x
                if len(b) != 0:
                    count+=1
                    caseid = '{}_{}'.format(l, count)
                writer.writerow((caseid,a,b,c,d))
            