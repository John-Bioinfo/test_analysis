#!/bin/bash


sort -u resTargets.list | grep "target" > fileslist

##filesl=$1

cat fileslist | while read vcfFile
do
    sample=$(echo ${vcfFile} | awk -F'/' '{print $8}')
    if [[ ! -e ${sample} ]]
    then 
        mkdir ${sample}
    fi
    a=$(basename ${vcfFile})
    cp ${vcfFile} ${sample}/${a}
done
