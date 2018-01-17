#!/usr/bin/perl
#
use strict;
use warnings;


my $infile=shift;


open(my $IN, "< $infile") || die("Can not open the GFF file! $! \n");

my $meta_info;
my $geneF;
my @array = ();

while(<$IN>){

    my $line = $_;
    chomp $line;
    if ($line =~ m/^#/){
        next;
    }
    @array = split (/\t/, $line);
    $meta_info = $array[8] ;
    $geneF = $array[2];
    
    if ($geneF eq "gene"){
        my $info = m/.*GeneID:(\d+?)[;,].*Name=(.*?);[\w\W]*/;

        my $ID = $1;
        my $Name = $2;

        print "$1\t$2\n";
    }
}

close $IN;
