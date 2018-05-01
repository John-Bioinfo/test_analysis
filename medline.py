from Bio import Entrez
from Bio import Medline

keyword = "Picoides pubescens"           ## define key words here

Entrez.email = "gulile@yeah.net"

handle = Entrez.esearch(db = "pubmed", term = keyword)

record = Entrez.read(handle)


pmids = record['IdList']

print(pmids)

handle = Entrez.efetch(db='pubmed', id = pmids, rettype = "medline", retmode = "text")

medline_records = Medline.parse(handle)

records = list(medline_records)

n = 1

f = open("results.txt", "w")

for record in records:
    print (n, ')', record['TI'])
    n += 1
    content = record['TI']
    f.write(content + "\n")

f.close()
    
