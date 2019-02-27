

docker run -iv  /data2/test:/data2/test/ hlasepa:latest samtools index test.bam

bash test_1.sh

python compare_GermLine_Mut.py positive_positions.txt

