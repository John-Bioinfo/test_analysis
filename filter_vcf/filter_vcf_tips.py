from collections import defaultdict

class VCFReaderEOFException(Exception):
	def __init__(self):
		pass
	def __str__(self):
		return "Format corruption in file to satisfy read request"

class VCFReader:
#DP=7;VDB=6.718756e-02;RPB=-6.486824e-01;AF1=0.5;AC1=5;DP4=2,2,1,2;MQ=20;FQ=10.3;PV4=1,0.12,1,0.46
	# Map well-known column names into struct format characters.

	def __init__(self, fileName):
		self.file = open(fileName,'r')
                self.InfoNames = {
                'DP': 1,
                'VDB': 1,
                'RPB': 1,
                'AF1': 1,
                'AC1': 1,
                'MQ': 1,
                'FQ': 1,
                         }
	def filter(self, field, v):
                vars_chr = defaultdict(list)
		for line in self.file:
		    cols = line.rstrip().split('\t')
                    if not line.startswith('#'):
                        info_values = cols[7].split(';')
                        d_info = {}
                        for j in info_values:
                            x = j.split('=')
                            if x[0] in self.InfoNames:
                                d_info[x[0]] = float(x[1])
                        var_i = d_info[field]
                        #print(var_i)

		        if var_i >= v:
			    vars_chr[cols[0]].append('\t'.join(cols[:2]))

                    else:
                        continue
		return vars_chr

	def __del__(self):
		self.file.close()

testReader = VCFReader('test_raw.vcf')

try:
	VarPacket = testReader.filter('DP', 30.0)
        var_num = 0

	for i in VarPacket:
		
		var_num += len(VarPacket[i])
	
	print('{0} variants'.format(var_num))
except VCFReaderEOFException:
	print('Error: File seems to be corrupted.')
