#!/bin/bash

fqfile=$1
SAMTOOLS=/root/anaconda3/bin/samtools
hlas_dir=/data2/test/lohhla_test/Test_620V3/ALL_hlas/

cat ${fqfile} | while read line
do
    fq1=${line}.1.fastq
    fq2=${line}.2.fastq

    sampleFullName=${line##*/}
    sampleName=$(echo ${sampleFullName} | awk -F'_' '{printf("%s-%s", $1,$2)}')
    
    hlas_sample=$(echo ${line} | cut -d'_' -f 3)
    if [[ ! -e  ${hlas_sample}_C.nix ]]
    then
        /root/anaconda3/bin/novoindex ${hlas_sample}_C.nix ${hlas_dir}/${hlas_sample}_hlas/types_C.fa
    fi
    if [[ ! -e out_${sampleName}_hlasC.sam ]]
    then    
        /root/anaconda3/bin/novoalign -d ${hlas_sample}_C.nix -f ${fq1} ${fq2} -F STDFQ -R 0 -r All 9999 -o SAM -o FullNW 1> out_${sampleName}_hlasC.sam 2> outC.${hlas_sample}.hlas.metrics    
    fi

    $SAMTOOLS view -@ 8 -bS out_${sampleName}_hlasC.sam | $SAMTOOLS sort - -@ 8 -T aln_tmp_sorted -o hlaC_${sampleName}_sorted.bam
    $SAMTOOLS index hlaC_${sampleName}_sorted.bam
    python pick_hlaC.py ${hlas_dir} ${hlas_sample}
    sleep 2
    $SAMTOOLS depth -b testHLA_1.bed hlaC_${sampleName}_sorted.bam -a > ${sampleName}_hlaC_1.dep
 
    $SAMTOOLS depth -b testHLA_2.bed hlaC_${sampleName}_sorted.bam -a > ${sampleName}_hlaC_2.dep
done



