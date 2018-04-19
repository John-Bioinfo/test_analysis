#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__      = "Zongyun Qiao"
__copyright__   = "Copyright 2018, A Biotech"
__credits__     = [
    "Zongyun Qiao"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.1-dev, 20180418"
__maintainer__  = "Zongyun Qiao"
__email__       = "gulile@yeah.net"

import shutil
import os

import subprocess

resultDir = "?Fusion-reanalysis/result-Fusion/Fusion_analysis/"

dep_script = "?python_scripts/extract_separate_FusionSams.py"
p_script =   "?python_scripts/testFusionPlots/plotFusion_breakPoints.R"

sampleS = [ "009",
            "010",
            "011",
            "012",
            "013",
            "014",
            "015",
            "016",
            "025",
            "026",
            "027",
            "028",
            "029",
            "030",
            "031",
            "032",
            "041",
            "042",
            "043",
            "044",
            "045",
            "046",
            "047",
            "048",
            "057",
            "058",
            "059",
            "060",
            "061",
            "062",
            "063",
            "064",
            "066",
            "073",
            "075",
            "076",
            "077",
            "078",
            "079",
            "080",
            "089",
            "090",
            "091",
            "092",
            "093",
            "094",
            "095",
            "096"
         ]


def Plot_sample(d_dir, pName):
    if not os.path.isdir(d_dir):
        sys.exit("Directory does not exist. Please check it.")
    T_files = []

    name_s = pName.split("*")

    # barcode = pName.replace(name_s[0], "").replace(name_s[1],"")
    for root, dirs, files in os.walk(d_dir):
        for fr in files:
            # if fr.endswith("Depth_Result.txt"):
            
            barcode = fr.replace(name_s[0], "").replace(name_s[1],"")
            if barcode in sampleS:
                f_path = os.path.join(root, fr)
                T_files.append(f_path)
                
                shutil.copy(f_path, fr)
                fusionTxt = os.path.join(root, "EML4_fusion_" + barcode + ".txt")
                fusionAP  = os.path.join(root, "AP_EML4_"     + barcode + ".sam")

                shutil.copy(fusionTxt,  "EML4_fusion_" + barcode + ".txt")
                shutil.copy(fusionAP ,  "AP_EML4_"     + barcode + ".sam")

                CallCalcDepCmd = "python %s -i %s -a %s -b %s -o %s"%(dep_script, "EML4_fusion_" + barcode + ".txt", fr, "AP_EML4_"     + barcode + ".sam" , "Sample" + barcode + ".txt")

                retcode = subprocess.call(CallCalcDepCmd, shell=True)
                if retcode == 0:
                    subprocess.call("Rscript %s %s"%(p_script, "Sample" + barcode + ".txt"), shell=True)

                print(CallCalcDepCmd)
                print("Rscript %s %s"%(p_script, "Sample" + barcode + ".txt"))

    return T_files
# 
#
# test: python extract_separate_FusionSams.py -i test_FusionFiles/EML4_fusion_080.txt -a test_FusionFiles/Aln_ALK.fa_080.sam -b test_FusionFiles/AP_EML4_080.sam -o Sample080.txt

##
## Rscript plotFusion_breakPoints.R Sample080.txt

z = Plot_sample(resultDir, "Aln_ALK.fa_*.sam")



