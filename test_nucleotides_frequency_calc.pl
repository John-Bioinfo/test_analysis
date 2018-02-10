#!/usr/bin/perl -w

use strict;
use warnings;

die "perl $0 <Ref_fa> <input_txt> <output> " unless @ARGV == 3;
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
     #print $count;
     for(my $j=0;$j<=$count-1;$j++){
     #print $hash{$chr};
          #print $hash{$keys[$j]}."\n";         
          $i=0;
          my $pos = 0;
          my $position = 0;
          while($pos != -1){
            
              $pos = index($hash{$keys[$j]},$sequence,$position);
#              print $hash{$keys[$j]}."\n";
#            print $sequence."\n";
#            print $pos."\n";
            #print $hash{$chr}."\n";
            #print $sequence."\n";
            if($pos == -1){
               last;
              }  #else{
              $i++;
               #print $pos."\n";
              $position = $pos + 5;
#              #print $i;
#           }
#          #$a += $i;
         }
#          $a += $i;
#          chomp($keys[$j]);
#          chomp($line);
#          chomp($sequence);
          print OUT $line."\t".$sequence."\t".$keys[$j]."\t".$i."\n";

      }
}
close OUT;
close IN;




