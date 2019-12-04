
import os
import subprocess
from glob import glob

dirs = glob("*_vars")

for v_dir in dirs:
    os.chdir(v_dir)
    sampleID = v_dir.split("_")[0]
    #allF = os.listdir("./")
    allF = glob("*.vcf")
    
    n_20  = 0
    n_1   = 0
    n_0_5 = 0
    
    a_vcf = open(allF[0], "r")
    
    outFile = "out_" + allF[0] + ".xls"
    oa = open(outFile, 'w')
    oa.write("chromosome\tgene\tmut_AF\tColor\n")
    for line in a_vcf:
        if not line.startswith("#"):
            
            kx = line.rstrip().split("\t")
            
            AF = float(kx[9].split(":")[2])
            Color = "C0"            
            if AF <= 0.2 and AF > 0.01:
                Color = "C1"    
                n_20 += 1
            elif AF <= 0.01 and AF > 0.005:
                Color = "C2"
                n_1 += 1
            elif AF <= 0.005:
                Color = "C3"
                n_0_5 += 1
            
            if Color != "C0":
                oa.write("{0}\t{1}\t{2}\t{3}\n".format(kx[0], kx[1], kx[9].split(":")[2], Color))
    oa.close()
    subprocess.call("python ../manha_readcsv.py %s %s" % (outFile, sampleID), shell=True)
    print("20% var number\t{0}".format(n_20))
    print("1% var number\t{0}".format(n_1))
    print("0.5% var number\t{0}".format(n_0_5))
    
    a_vcf.close()
    os.chdir("../")
