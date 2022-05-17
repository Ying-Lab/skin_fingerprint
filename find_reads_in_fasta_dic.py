import os
import numpy as np
import random
import pandas as pd
from multiprocessing import Process

def get_file_name(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #判断后缀
            if os.path.splitext(file)[1] == '.sam':
                name = os.path.splitext(file)[0]
                file_list.append(name)
    #print (len(file_list),sorted(file_list))
    file_list_temp = list(file_list)
    new_file_list = list(set(file_list_temp))
    return sorted(new_file_list)
    #return file_list

def get_file_reads(dic,sam_file):
    key_list = []
    old_key_list = sorted(list(dic.keys()))
    for i in old_key_list:
        if len(dic[i]) > 1:
            key_list.append(i)
    key_list = sorted(key_list)
    #print (len(key_list), key_list)
    #print(len(key_list))
    #print(key_list[:10])

    # 打开原fasta文件
    with open('/path/'+sam_file,'r') as fa:
        s = fa.readline()[:-1]
        while s != '':
            #key_list = list(dic.keys())
            skey = s[1:s.find(' ')]
            if skey in dic and len(dic[skey])>1:
            #for i in key_list:
                #print(i)
                # for i in dic.keys()[:50]:
                #if len(dic[i]) > 1:
                if s[:len(skey)+1] == '>'+skey and s[len(skey)+1] == ' ':
                    print (skey)
                    # 每条reads与specific_kmer匹配的情况
                    f = open(pe_reads_path+'read_test_'+sam_file+'.txt','a')
                    f.write(skey+'\tspecific_kmer_number = '+str(len(dic[skey]))+'\n')
                    s = fa.readline()[:-1]
                    f.write(s)
                    #print (s)
                    s = fa.readline()[:-1]
                    f.write(s)
                    #print (s)
                    s = fa.readline()
                    f.write(s)
                    #print (s)
                    #s = fa.readline()[:-1]
                    f.close()
            s = fa.readline()

def process_fuc(sam_file, sam_file_path):
    print ('sam_file = ',sam_file)
    dic = {}
    file_path = sam_file_path+sam_file+'.sam'
    f = open(file_path,'r')
    s = f.readline()[:-1]
    while s != '':
        if s.split()[5] == '31M' and (int(s.split()[3])<71 or int(s.split()[3])>101):
            if s.split()[2] not in dic:
                dic[s.split()[2]] = [s.split()[0]]
            else:
                dic[s.split()[2]].append(s.split()[0])

            s = f.readline()[:-1]
        else:
            s = f.readline()[:-1]

    f.close()
    get_file_reads(dic,sam_file)


if __name__ == "__main__":

    sam_file_path = ''
    pe_reads_path = ''
    se_read_path = ''
    ultimately_read_path = ''

    os.system('mkdir '+pe_reads_path)
    os.system('mkdir '+se_read_path)
    sam_file_list = get_file_name(sam_file_path)
    #sam_file_list = ['HV08_13-01-16_Hp-R_Ss_dry.fasta']
    print (len(sam_file_list),sam_file_list)
    #0-29
    #sam_file = 'HV08_13-01-16_Al-R_Ss_sebaceous.fasta'

    jobs = [Process(target=process_fuc, args=(
        sam_file, sam_file_path))
        for sam_file in sam_file_list]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join    ()

    SRR_reads_file_list = []
    for root, dirs, files in os.walk(pe_reads_path):
        for file in files:
            # 判断后缀
            if os.path.splitext(file)[1] == '.txt':
                name = os.path.splitext(file)[0]
                # name 是没有后缀名的 file是带有后缀名的
                SRR_reads_file_list.append(file)
    SRR_reads_file_list = sorted(SRR_reads_file_list)
    print (len(SRR_reads_file_list), sorted(SRR_reads_file_list))

    for file in SRR_reads_file_list:
        # f = open('/home/yingwang/zyl/bowtie/reads_file/read_test_HV08_13-01-16_Ic-R_Ss_moist.fasta.txt','r')
        f = open(pe_reads_path + file, 'r')
        s = f.readline()[:-1]
        while s != '':
            if s[0] == 'S':
                count = 1
                with open(se_read_path+'split_' + file[10:-4] + '.fasta', 'a') as f1:
                    read_name = s.split()[0]
                    f1.write('>' + read_name + '_' + str(count) + '\n')
                    s = f.readline()
                    read1 = s[:101]
                    read2 = s[101:]
                    f1.write(read1 + '\n')
                    count += 1
                    f1.write('>' + read_name + '_' + str(count) + '\n')
                    f1.write(read2)
                    # f1.write(s)
                s = f.readline()[:-1]
            else:
                s = f.readline()[:-1]
        f.close()

