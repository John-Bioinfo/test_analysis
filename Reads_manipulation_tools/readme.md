## Extract Sam/Bam to Dat

- samtools index *.sam > *.dat
or
- docker run -iv  /data2/test:/data2/test/ hlasepa:latest samtools view *.bam > *.dat

## Count Reads at certain genome position

- python extract_sites.py *.dat
