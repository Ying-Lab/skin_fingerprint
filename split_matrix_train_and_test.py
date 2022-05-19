from itertools import chain
from multiprocessing import Process
import os
import random
import copy

random.seed(0)

# 过滤不要的部位 比如足部数据
def fitering_site(inputname, site_list):
    body_all = [[] for i in range(5)]
    fi = open(inputname, 'r')
    s = fi.readline().strip()
    s = s.split('\t')
    s = s[1:]
    # i 是文件名 id是序列号
    for id, i in enumerate(s):
        if i in small_file:
            continue
        else:
            flag = False
            for j in site_list:
                if i.find(j) != -1:
                    flag = True
                    break
            if flag == False:
                body_all[int(i[2:4])-1].append('%d-%d' % (id + 2, id + 2))
    fi.close()

    return body_all


# 区分A类B类，并划分train and test （建立一个train_test_matrix 并返回
def train_test_split():
    # 筛选掉不要的部位 []则使用全部数据
    # all 中按人存放数据对应完整大矩阵（616个文件）的索引
    all = fitering_site(os.path.join(inputpath, 'son_matrix_0.txt'), ['-5'])
    print (len(all), all)
    train_file_matrix, test_file_matrix = [], []
    A_all = all[0]  # 筛选部位之后剩下的A类文件
    B_all = all[1:]  # 其余11个人也筛选部位之后剩下的B类所有文件，一个矩阵，一行是一个人
    print ('len A_all = ', len(A_all), A_all)
    print ('lem B_all = ', len(B_all[0]), B_all)
    # A类的train 35个 test为剔除某些部位后所剩下的fasta文件
    # B类的train 44个 test为22个 （总计每个人都抽6个）
    group_A = copy.deepcopy(A_all)
    group_B = copy.deepcopy(B_all)
    for i in range(3):
        A_train_reserve = random.sample(group_A, train_groupA_number)
        group_A = list(set(group_A) - set(A_train_reserve))
        A_test_reserve = list(set(A_all) - set(A_train_reserve))
        B_train_reserve = []
        B_test_reserve = []
        for b in range(len(group_B)):
            gb = random.sample(group_B[b], train_groupA_number)
            B_train_reserve = B_train_reserve + gb
            group_B[b] = list(set(group_B[b]) - set(gb))
        B_test_reserve = list(set(list(chain.from_iterable(B_all))) - set(B_train_reserve))
        # '''
        print(len(A_train_reserve), 'A_train = ', A_train_reserve)
        print(len(A_test_reserve), 'A_test = ', A_test_reserve)
        print(len(B_train_reserve), 'B_train = ', B_train_reserve)
        print(len(B_test_reserve), 'B_test = ', B_test_reserve)
        # '''
        # 原始矩阵被保留的列数
        reserve_column_StrList_train = ['1-1'] + A_train_reserve + B_train_reserve  # train
        reserve_column_StrList_test = ['1-1'] + A_test_reserve + B_test_reserve  # test
        train_file_matrix.append(reserve_column_StrList_train)
        test_file_matrix.append(reserve_column_StrList_test)

    return train_file_matrix, test_file_matrix


def StrList2List(reserve_column_StrList_train, reserve_column_StrList_test):
    # global reserve_column_list_train,reserve_column_list_test
    reserve_column_list_train, reserve_column_list_test = [], []
    for i in reserve_column_StrList_train:
        for j in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1):
            reserve_column_list_train.append(j - 1)
    for i in reserve_column_StrList_test:
        for j in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1):
            reserve_column_list_test.append(j - 1)
    print ('the number of train file = ', len(reserve_column_list_train) - 1, 'reserve_column_StrList_train = ',
           reserve_column_StrList_train)
    print ('the number of test file = ', len(reserve_column_list_test) - 1, 'reserve_column_StrList_test = ',
           reserve_column_StrList_test)
    return reserve_column_list_train, reserve_column_list_test


# 切割 train set 矩阵
def SplitMatrix_for_train(number, inputname, outputname, outputfname, reserve_column_list, groupA_number, ASS_thr):
    fi = open(inputname, 'r')
    fo = open(outputname, 'w')
    fof = open(outputfname, 'w')
    if not fi:
        print('input error!')
    elif not fo:
        print('output error!')
    elif not fof:
        print('output f error!')
    else:
        cnt = 0
        s = fi.readline().strip()
        if number == 0:
            print ('all_orginal_file_name = ', s)
        s = s.split('\t')
        groupA_idx_list = []
        groupB_idx_list = []
        wline = ''
        for i in range(len(s)):
            if i in reserve_column_list:
                wline += s[i] + '\t'
                if s[i][:4] == 'HV01':
                    groupA_idx_list.append(i)
                elif s[i][:2] == 'HV':
                    groupB_idx_list.append(i)

        wline = wline + 'ASS\n'
        fo.write(wline)
        if number == 0:
            print ('train_file_name = ', wline)

        s = fi.readline().strip()
        while s != '':
            s = s.split('\t')
            wline = ''
            allnum = -1
            gA = 0;
            gB = 0
            for i in range(len(s)):
                if i in reserve_column_list:
                    allnum += 1
                    wline += s[i] + '\t'
                    if i == 0:
                        continue
                    if i in groupA_idx_list:
                        if s[i] != "0":
                            gA += 1
                    elif i in groupB_idx_list:
                        print(s[i])
                        if s[i] == "0":
                            gB += 1
            ass = (gA / groupA_number + gB / (allnum - groupA_number)) / 2
            wline = wline + str(ass) + '\n'
            fo.write(wline)
            if ass >= ASS_thr:
                cnt += 1
                fof.write(s[0] + '\t' + str(ass) + '\n')
            s = fi.readline().strip()
    fi.close()
    fo.close()
    fof.close()


# 切割 test set 矩阵
def SplitMatrix_for_test(number, inputname, outputname, reserve_column_list, groupA_number):
    fi = open(inputname, 'r')
    fo = open(outputname, 'w')
    if not fi:
        print('input error!')
    elif not fo:
        print('output error!')
    else:
        cnt = 0
        s = fi.readline().strip()
        s = s.split('\t')
        groupA_idx_list = []
        groupB_idx_list = []
        wline = ''
        for i in range(len(s)):
            if i in reserve_column_list:
                if s[i][:4] == 'HV01':
                    groupA_idx_list.append(i)
                elif s[i][:2] == 'HV':
                    groupB_idx_list.append(i)
                wline += s[i] + '\t'
        wline = wline + 'A_acc\tB_acc\n'
        fo.write(wline)
        if number == 0:
            print ('test_file_name = ', wline)

        s = fi.readline()[:-1]
        while s != '':
            s = s.split('\t')
            wline = ''
            allnum = -1;
            gA = 0
            gB = 0
            # gA 是A组中非0的个数 gB是B组中为0的个数
            for i in range(len(s)):
                if i in reserve_column_list:
                    wline += s[i] + '\t'
                    allnum += 1
                    if i == 0:
                        continue
                    if i in groupA_idx_list:
                        if s[i] != "0":
                            gA += 1
                    elif i in groupB_idx_list:
                        if s[i] == "0":
                            gB += 1
            A_acc = gA / groupA_number
            B_acc = gB / (allnum - groupA_number)
            # ass = (gA / groupA_number + gB / (allnum - groupA_number)) / 2
            wline = wline + str(A_acc) + '\t' + str(B_acc) + '\n'
            fo.write(wline)
            s = fi.readline().strip()

    fi.close()
    fo.close()


# 在test matrix中寻找train的specific kmer所在行
def find_kmer(number, input_path, output_path):
    fi = open(input_path + '/out_split_matrix_' + str(number) + '.txt', 'r')
    fo = open(output_path + '/specific_kmer_matrix_' + str(number) + '.txt', 'w')
    s = fi.readline()  # 先读第一行 样本名
    fo.write(s)  # 第一次时样本名写入specific_kmer矩阵的第一行
    s = fi.readline()[:-1]  # 读第二行
    while s != '':
        kmer_in_test = s.split()[0]
        if kmer_in_test in kmer_dic:
            fo.write(s + '\n')
        s = fi.readline()[:-1]  # 开始读 specific kmer
    fi.close()
    fo.close()


if __name__ == '__main__':
    ASS_thr = 0.8
    n = 16
    HV = 'HV01'
    train_groupA_number = 2  # 训练集的A类的个数 取决于删除的数据
    test_groupA_number = 4  # 测试集的A类的个数


    # input是完整的大矩阵，617列 kmer+616个无.fasta的文件名
    inputpath = './kmer_matrix'
    os.system('mkdir -p ./train')
    os.system('mkdir -p ./test')

    # 需要过滤的小样本
    small_file = ['HV02_1']

    train_file_matrix, test_file_matrix = train_test_split()  # 记得筛选不要的部位

    train_reserve_column_matrix, test_reserve_column_matrix = [], []
    for time in range(0, 3):
        print (str(time + 1))
        os.system('mkdir -p ./train/'+ str(time + 1))
        os.system('mkdir -p ./test/' + str(time + 1))
        # 路径下的out_matrix_ 第一列是 kmer 最后一列是ass
        train_outputpath = './train/' + str(time + 1)
        test_outputpath = './test/' + str(time + 1)
        reserve_column_list_train, reserve_column_list_test = StrList2List(train_file_matrix[time],
                                                                           test_file_matrix[time])
        # train_reserve_column_matrix.append(reserve_column_list_train)
        # test_reserve_column_matrix.append(reserve_column_list_test)

        print(len(reserve_column_list_train))
        print ('reserve_column_list_train = ', reserve_column_list_train)
        print(len(reserve_column_list_test))
        print ('reserve_column_list_test = ', reserve_column_list_test)
        
        # ========== for train===================
        jobs = [Process(target=SplitMatrix_for_train, args=(i,
                                                            os.path.join(inputpath, 'son_matrix_' + str(i) + '.txt'),
                                                            os.path.join(train_outputpath,
                                                                         'out_split_matrix_' + str(i) + '.txt'),
                                                            os.path.join(train_outputpath,
                                                                         'out_kmer_ass_filt_matrix_' + str(i) + '.txt'),
                                                            reserve_column_list_train, train_groupA_number, ASS_thr))
                for i in range(n)]
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

        # ========== for test===================
        jobs = [Process(target=SplitMatrix_for_test, args=(i,
                                                           os.path.join(inputpath, 'son_matrix_' + str(i) + '.txt'),
                                                           os.path.join(test_outputpath,
                                                                        'out_split_matrix_' + str(i) + '.txt'),
                                                           reserve_column_list_test, test_groupA_number))
                for i in range(n)]
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

        # 合并 train_specific_kmer.txt
        os.system(
            'cat ' + train_outputpath + '/out_kmer_ass_filt_matrix_* > ' + train_outputpath + '/train_specific_kmer.txt')
        # os.system('cat '+train_outputpath + '/train_specific_kmer.txt | grep "0.9" > '+train_outputpath + '/train_specific_kmer_09.txt')
        os.system(
            ' cat ' + train_outputpath + '/train_specific_kmer.txt | awk -v OFS=\'\\t\' \'{if($NF>=0.9)print $1,$NF}\' > ' + train_outputpath + '/train_specific_kmer_09.txt')
        os.system(
            'cat ' + train_outputpath + '/out_split_matrix_15.txt | head -n 1 | sed \'s/\\t/\\n/g\' > '+train_outputpath+'/file_name.txt')
        os.system('sed -i \'1d\' ' + train_outputpath + '/file_name.txt')
        os.system('sed -i \'31,$d\' ' + train_outputpath + '/file_name.txt')

        # 读train 的 specific_kmer的TXT文件
        kmer_list = []
        kmer_dic = {}
        f_kmer = open(train_outputpath + '/train_specific_kmer_09.txt', 'r')
        s = f_kmer.readline()[:-1]
        while s != '':
            kmer = s.split('\t')[0]
            kmer_dic[kmer] = 0
            s = f_kmer.readline()
        f_kmer.close()

        # 多线程在测试集矩阵中寻找训练集的specific_kmer
        jobs = [Process(target=find_kmer, args=(i, test_outputpath, test_outputpath))
                for i in range(n)]
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

        os.system('cat ' + test_outputpath + '/specific_kmer_matrix_*.txt > ' + test_outputpath + '/all_specific_kmer_matrix.txt')
        os.system('awk -v OFS=\'\\t\' \'{print $1,$(NF-1),$NF,($(NF-1)+$NF)/2}\' '+ test_outputpath + '/all_specific_kmer_matrix.txt  >' + test_outputpath + '/kmer_details.txt')


    for time in range(3):
        train_outputpath = './train/' + str(time + 1)
        test_outputpath = './test/' + str(time + 1)
        kmer_list, train_ass_list = [], []
        f1 = open(train_outputpath + '/train_specific_kmer_09.txt', 'r')
        s = f1.readline()
        while s != '':
            kmer = s.split()[0]
            train_ass = s.split()[1]
            train_ass_list.append(train_ass)
            kmer_list.append(kmer)
            s = f1.readline()
        f1.close()
        print ('len of train kmer = ', len(kmer_list))

        f2 = open(test_outputpath + '/kmer.txt', 'r')
        f3 = open(test_outputpath + '/' + '_train' + str(time + 1) + '_kmer_ass_in_train_test.txt', 'a')
        # s=f2.readline()
        s = f2.readline()[:-1]
        while s != '':
            kmer = s.split()[0]
            test_ass = s.split()[-1]
            print(test_ass)
            if kmer in kmer_list:
                f3.write(s + '\t' + str(train_ass_list[kmer_list.index(kmer)]) + '\n')
            s = f2.readline()[:-1]
        f2.close()


