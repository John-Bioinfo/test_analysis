#!/usr/bin/perl
#
use strict;
use warnings;
use List::Util qw(sum);


$/='>';
my $fafile = shift;

my @faLens = ();
open(my $SC, "<$fafile");
while (my $seq = <$SC>){
    $seq =~ s/>$//;
    $seq =~ s/^(.*)//;
    my $id = $1;
    $seq =~ s/\n//g;
    my $falen = length($seq);
    push @faLens, $falen;
    #print "$falen\n";
}

my @LenArrs = sort {$b <=> $a} @faLens;

my $totLen = sum(@LenArrs);

my $lenSum = 0;

foreach my $l (@LenArrs){
    $lenSum += $l;
    if($lenSum >= $totLen/2){print "$l\n";last;}
}
