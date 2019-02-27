#!/bin/bash

wd=`pwd`
for i in `ls -l ./ |awk '/^d/ {print $NF}'`
do
    fdir=${wd}/${i}
    a=`ls ${fdir}/*.bam 2>/dev/null`
    if [[ ! -z "${a}" ]];
    then
        n=1
        echo "docker run -iv  /data2/test:/data2/test/ hlasepa:latest samtools index ${a}" > ${fdir}/test.sh
        for vcf in `ls ${fdir}/*.vcf`
        do
            cat >> ${fdir}/test.sh << EOF

docker run -iv /data2:/data2 biotk:latest  /opt/jvm/jdk1.8.0_102/bin/java -Xmx1g -jar /bio/gatk3.7/GenomeAnalysisTK.jar  -T MuTect2  -I:tumor ${a}  -R /data2/test/zyqiao_test/mut_compare/c_bam/reffiles/hg19.fasta  --dbsnp /data2/test/zyqiao_test/mut_compare/c_bam/reffiles/dbsnp_138.hg19.vcf  -L ${vcf} --disableOptimizations --dontTrimActiveRegions --forceActive -bamout ${fdir}/${i}_bamou${n}.bam -ip 100


EOF
            n=$(($n+1))
        done
    fi
done
