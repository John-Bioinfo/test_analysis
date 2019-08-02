## Extract Sam/Bam to Dat

- samtools index *.sam > *.dat
or
- docker run -iv  /data2/test:/data2/test/ hlasepa:latest samtools view *.bam > *.dat

## Count Reads at certain genome position

- python extract_sites.py *.dat 

or 

- python extract_sites_new.py *.dat
- python generate_html.py test_con_mut_reads.txt > test1.html
