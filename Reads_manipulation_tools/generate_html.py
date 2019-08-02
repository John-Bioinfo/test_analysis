#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys


def get_seq(seq_file):
    
    f_h = open(seq_file, 'r')
    s_List = []
    for line in f_h:
        seq = line.rstrip()
        s_List.append(seq)

    return s_List

def print_head(file_t, left_width, right_width):

    head = """<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">
<title>%s Test</title>

<h2>NGS Reads - SNP</h2>
<style type="text/css">
#BigBox{
    width:%spx;
    height:1800px;
  }
#bigBox_left{
    width:%spx;
    height:1800px;
    float:left;
  }
#bigBox_right{
    border:2px solid Gray;
    width:%spx;
    height:1800px;
    float:right;
    margin:50px auto;
  }#seqBOX{
    border:1px solid white;
    width:%spx;
    height:20px;
    margin:40px auto;
  } 
#boxA{
               background:yellow;
               width:12px;
               height:20px;
               display: inline-block
}#boxT{
               background:SkyBlue;
               width:12px;
               height:20px;
               display: inline-block
}#boxG{
               background:pink;
               width:12px;
               height:20px;
               display: inline-block
}#boxC{
               background:red;
               width:12px;
               height:20px;
               display: inline-block
}#boxN{
               background:grey;
               width:12px;
               height:20px;
               display: inline-block
}</style>
    </head>\n"""%(file_t, left_width + right_width + 40, left_width, right_width, right_width - 50)
    print(head)

sequences = get_seq(sys.argv[1])

s = sorted(sequences)
if len(sys.argv) >2 :
    print_head(sys.argv[2], 400, 6000)
else:
    print_head("", 400, 6000)


print("""
<body>
<div id="BigBox">
<div id="bigBox_left"><img src="images/DNA_doubleHelix.jpg" width=360px height=600px></div>
<div id="bigBox_right">""")

for n,i in enumerate(s):
    ID = "{0:04d}".format(n) 
    
    print("""
</br>
<div id="seqBOX">
<h4>Gene sequence: """ + ID + """</h4>
&nbsp;&nbsp;&nbsp;&nbsp;""" + "testSEQ--ATGC" + """</br>\n""")
    for j in i:
        if j == "*":
            base='N'
        else:
            base=j
        print('<div id="box' + base +'">' + base+'</div>')

    #print("""<p align="left">----------------- Gene END </p>
    print("""
</div>
</br>""")


print("""</div>
</div>
</body>
</html>""")
