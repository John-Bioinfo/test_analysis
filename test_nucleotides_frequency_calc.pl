#!/usr/bin/perl -w

use strict;
use warnings;

die "perl $0 <Ref_fa> <input_txt> <output> " unless @ARGV == 3;

## perl test_nucleotides_frequency_calc.pl test.fa length_5.txt length_freq.txt
## test.fa is chromosome sequence or other longer sequences in fasta format
## length_5.txt is 5bp nucleotides in fasta format

##
##>5_5
##AAATA
##>5_6
##AAATT
##>5_7
##AAATC
##>5_8
##AAATG
##>5_9
##AAACA
##
## length_freq.txt is output file

my $Ref_fa = shift;
my $in = shift;
my $out = shift;
my %hash=();
my $name;

if(-e "$out"){
    print "output File exists, please check it!\nNo data will be processed.\n";
    exit;
}

open (OUT,">>$out");
open (IN,"$Ref_fa") || die "Can't open $Ref_fa!\n";
while(my $line1=<IN>){
      chomp $line1;
#      print $line1;
      if ($line1 =~ ">"){
           $name=$line1;
           $hash{$name}="";
        }else{
           $hash{$name}.=$line1;
          }
}
#print values($hash{$name});
close IN;

my @keys= keys %hash;

my $i;
my $line;
my $sequence;

open (IN,"$in") || die "Can't open $in!\n";
while($line=<IN>){
    $sequence = <IN>;
    chomp $line;
    chomp $sequence;
     #foreach $chr (@keys){
     
     my $count = keys %hash;

     for(my $j=0;$j<=$count-1;$j++){
        
          $i=0;
          my $pos = 0;
          my $position = 0;
          while($pos != -1){
            
              $pos = index($hash{$keys[$j]},$sequence,$position);
#              print $hash{$keys[$j]}."\n";

            if($pos == -1){
               last;
              }  
              $i++;

              $position = $pos + 5;

         }

          print OUT $line."\t".$sequence."\t".$keys[$j]."\t".$i."\n";

      }
}
close OUT;
close IN;




