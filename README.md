# Individual specific skin fingerprint

We proposed a framework to capture individual-specific DNA microbial fingerprints from 616 skin metagenomic sequencing data. The fingerprints are identified on the frequency of 31-mers free from reference genomes and sequence alignments. Ultimately, one contig for each individual is assembled as a fingerprint. And results showed that 89.78% of the skin samples despite of body sites could identify their donors correctly. 

An demo of fingerprint running is given here.

### Running on Linux
1. If you first use, please type the command:

	*`sudo chmod +x ./bin/*`* 

2. Get kmer matrix of all data

	*`python3 KmerGO_for_cmd.py [optional options] -i <input_files_folder> -t <input_trait_information>`* 

3. Split dataset and get individual-specific kmer in details. 

	*`python3 split_matrix_train_and_test.py`*

4.Processing file formats for subsequent runs.

	*`python3 get_kmer.py`*

5. Obtain individual-specific contigs.

	*`./bin/cap3 <input_files>  -i 30  -j 31  -o 18  -s 300 `* 


### The demo of fingerprint on testing dataset.

The dataset was randomly generated. There were 20 contigs only exists in HV01.[Testing dataset Download](https://github.com/zhengyl2019/skin_fingerprint/tree/main/Demo_data)

1. Get kmer matrix of all data, the results save in **./kmer_matrix/son_matrix_*.txt**.
	*`python3 KmerGO_for_cmd.py -k 25 -ci 1 -cs 1000000000 -n 16 -i ./Demo_data -t trait information.csv`* 

2. Split dataset to train and test and save individual specific kmer with details in **train_specific_kmer_09.txt** for training data and **kmer_details.txt** for testing data.
	*`python3 split_matrix_train_and_test.py`*

3. Processing file formats for subsequent runs. The output file is **output_kmer.fa**.
	*`python3 get_kmer.py`*

4. Using software(cap3) to obatin individual-specific contigs. The contigs file is under the same path as the **output_kmer.fa** file with name **output_kmer.fa.cap.contigs**.
	*`./bin/cap3 output_kmer.fa  -i 30  -j 31  -o 18  -s 300 `* 


## Contacts and bug reports

Please send bug reports, comments, or questions to

Prof. Ying Wang: [wangying@xmu.edu.cn](mailto:wangying@xmu.edu.cn)

Yiluan Zheng: [23220191151270@stu.xmu.edu.cn](mailto:23220191151270@stu.xmu.edu.cn)

