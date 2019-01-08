

SAMTOOLS=/home/samtools/samtools

samples=(1821052 1821056 1821028)

for s in ${samples[@]}
do

    $SAMTOOLS index /data2/test/lohhla_test/wes_data/bam/${s}.dup.bam
    

    $SAMTOOLS depth -b hla_A.bed /data2/test/lohhla_test/wes_data/bam/${s}.dup.bam > ${s}_hlaA.dep

    $SAMTOOLS depth -b hla_B.bed /data2/test/lohhla_test/wes_data/bam/${s}.dup.bam > ${s}_hlaB.dep

    $SAMTOOLS depth -b hla_C.bed /data2/test/lohhla_test/wes_data/bam/${s}.dup.bam > ${s}_hlaC.dep
done
