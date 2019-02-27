#!/bin/bash

workDir=/data2/test/zyqiao_test/mut_compare/pisces_test
samples=(1910104 1910103 1810993 1910034 1910165 1910209 1910076 1910036 1910044 1910176 1910110 1910011)

for data in ${samples[@]}

do

    docker run -itv /data2/test:/data2/test/ hlasepa:latest dotnet /root/pisces/Pisces_5.2.9.122/Pisces.dll --bam ${workDir}/${data}/${data}.recal-H.bam -g /data2/test/zyqiao_test/mut_compare/pisces_test/fasta_Ref -crushvcf true -gVCF false -i /data2/test/zyqiao_test/mut_compare/pisces_test/83_gene/83gene.intervals -ploidy diploid -OutFolder ${workDir}/res_${data}_germline -RMxNFilter 5,9,0.35 


done
