import sys
import argparse
from collections import deque

Emer =  {   "AA": -1.94,
            "AC": -1.34,
            "AG": -1.6,
            "AT": -1.47,
            "CA": -1.95,
            "CC": -3.07,
            "CG": -3.61,
            "CT": -1.6,
            "GA": -1.57,
            "GC": -3.14,
            "GG": -3.07,
            "GT": -1.34,
            "TA": -0.96,
            "TC": -1.57,
            "TG": -1.95,
            "TT": -1.94    }
#Energy of polymer
complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}


def read_fasta(file_Name):
    fp = open(file_Name, "r")
    name, seq = (None, [])
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name:
                yield (name, ''.join(seq))
            name, seq = (line, [])
        else:
            seq.append(line.upper())
    if name:
        yield (name, ''.join(seq))

    fp.close()

def parse_table(file_Name):

    fp = open(file_Name, "r")
    n, s = (None, None)
    for line in fp:
        ax = line.rstrip().split("\t")
        if line.startswith("gene_name"):
            continue
        else:
            n = ax[1].replace("biotin-tr30P1", "")
            s  = ax[2]

            yield (n, s)

    fp.close()

def calcDg(list1, list2):
    m = len(list1)
    n = len(list2)
    U1 = list1.upper()
    U2 = list2.upper()
    d = deque()
    d.extendleft(U2)
    U2N = ''.join(d)
    reverse_N = "".join(complement.get(base, base) for base in U2N)
    L = set()
    for a in range(m-2):
        subU1 = U1[a:]
        subM = len(subU1)
        for a_end in range(2,subM+1):
            #L.append(subU1[:a_end])
            subNew = subU1[:a_end]
            if subNew in reverse_N:
                L.add(subNew)

    dG = []
    for b in L:
        g = 0
        for i in range(len(b)-1):
            g += Emer[b[i:i+2]]
        #dG.append("{0:.2f}".format(g))
        dG.append(g)
    return(dG)

def GCCalc(seq):
    GC_Content = seq.count("C") + seq.count("G")
    formGC = "{0:.2f}".format( GC_Content * 100.0 / len(seq) )
    return formGC

def TemMelt(seq):
    sGC = (seq.count("C") + seq.count("G"))*1.0 / len(seq)
    con005_T = 59.9 + 41.0 * sGC - (675.0/len(seq))

    con1_T   = 81.5 + 41.0 * sGC - (675.0/len(seq))
    
    return ("{0:.3f}".format(con005_T), "{0:.3f}".format(con1_T))

def Score_Func(xList):
    
    coe  = 0
    mHigh = xList[0]

    mostH_num = xList.count(mHigh)
 
    coe += mostH_num
    for num, f in enumerate(xList[mostH_num:]):
        ##a = f * 1.0 / mHigh
        a = f * 1.0 / 50
        coe += a / (num + 1 + mostH_num)

    return 100.0/ coe

if __name__ == '__main__':
    HELP = """USAGE: python {0} -i inputFile -c combination_probesFile """.format(__file__)

    parser = argparse.ArgumentParser( description = HELP )

    parser.add_argument("-c", "--comp", action="store", required=True, help="comparison probes")
    parser.add_argument("-i", "--inputf", action="store", help="analysis seq file")
    args = parser.parse_args()

    testIn = args.inputf
    cfile = args.comp

    # Test Command : python combinations_probe_screen.py -c Test_Dec.txt -i test_In.fa

    if testIn == None:
        print(HELP)
        sys.exit("input file is not provided, please check it.")

    f_handle = open(testIn, "r")

    for line in f_handle:

        ax = line.strip().split("\t")
        seqID = ax[0].replace("testP_", "")
        seq = ax[1]
        splitScore = ax[2].split(",")
        BlastS = [float(i) for i in splitScore]
        xs1 = Score_Func(BlastS)

        sGC = GCCalc(seq)
        T005, T1 = TemMelt(seq)
        H_dg = []
        for cseqId, cseq in parse_table(cfile):
        #testDg = "{0:.3f}".format(min(calcDg(seq, cseq)))
            testDg = min(calcDg(seq, cseq))
            H_dg.append(testDg)

        sortDg = sorted(H_dg, reverse=True)
        maxDgs = sortDg[0:2] 
        minDgs = sortDg[-2:]

        Dmax = sum(maxDgs)/2
        Dmin = sum(minDgs)/2
        S_dg = "{0:.3f}".format(min(calcDg(seq, seq)))
    #all_HeteroG = ",".join(H_dg)
    
        print(seqID, seq, sGC, T005, T1, S_dg,"{0:.3f}".format(Dmax), "{0:.3f}".format(Dmin) , xs1)

    f_handle.close()
