f = open('/home/yingwang/zyl/demo_test/test/3/kmer_details.txt', 'r')
fo = open('output_kmer.fa', 'w')
cnt = 0
while True:
	s = f.readline().strip()
	if s == '':
		break
	kmer = s.split('\t')[0]
	if kmer != 'k-mer':
		cnt += 1
		fo.write('>'+str(cnt)+'\n'+kmer+'\n')
f.close()