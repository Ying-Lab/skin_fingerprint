# Individual specific skin fingerprint

We proposed a framework to capture individual-specific DNA microbial fingerprints from 616 skin metagenomic sequencing data. The fingerprints are identified on the frequency of 31-mers free from reference genomes and sequence alignments. Ultimately, one contig for each individual is assembled as a fingerprint. And results showed that 89.78% of the skin samples despite of body sites could identify their donors correctly. 

An demo of fingerprint running is given here.

### Running on Linux

You can type *`sudo chmod +x ./bin/*`*  if you first use.

You can type *`python3 KmerGO_for_cmd.py -k 25 -ci 1 -cs 1000000000 -n 16 -i ./Demo_data -t trait information.csv`* to get kmer matrix of all data.

You can type *`python3 split_matrix_train_and_test.py`* to split dataset and save individual specific kmer with details in files.

You can type *`bowtie2-build --large-index -f <kmer file> <path of bowtie index> --threads 4`* to use bowtie and then type *`python3 find_reads_in_fasta_dic.py`* to find reads that contain at least 2 specific kmers, and save these reads in a file.

You can type *`magahit --12 reads.fasta -o output `* to obatin individual-specific contigs.

###The demo of fingerprint on testing dataset.
The dataset was randomly generated. There were 20 contigs only exists in HV01.

You can type *`python3 KmerGO_for_cmd.py -k 25 -ci 1 -cs 1000000000 -n 16 -i ./Demo_data -t trait information.csv`* to get kmer matrix of all data.

You can type *`python3 split_matrix_train_and_test.py`* to split dataset and save individual specific kmer with details in files.

You can type *`bowtie2-build --large-index -f <kmer file> <path of bowtie index> --threads 4`* to use bowtie and then type *`python3 find_reads_in_fasta_dic.py`* to find reads that contain at least 2 specific kmers, and save these reads in a file.

You can type *`magahit --12 reads.fasta -o output `* to obatin individual-specific contigs.

## Contacts and bug reports

Please send bug reports, comments, or questions to

Prof. Ying Wang: [wangying@xmu.edu.cn](mailto:wangying@xmu.edu.cn)

Yiluan Zheng: [23220191151270@stu.xmu.edu.cn](mailto:23220191151270@stu.xmu.edu.cn)

