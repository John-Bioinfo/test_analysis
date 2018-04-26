#!/usr/bin/perl
#
use warnings;
use strict;

$/='>';
my $fafile = shift;
#print "$fafile\n";

my @faLens = ();

open(my $SC, "<$fafile");
while (my $seq = <$SC>){
    my $s = $seq;
    
    $seq =~ s/>$//;
    $s =~ s/^(.*)//;
    my $id = $1;
    $s =~ s/\n//g;

    my $falen = length($s);
    if( $falen >200){
        my $GCcount1 = 0;
        ## $s1 = substr $s, 0, 200;
        #print ">$id\n$s\t";
        my @ida = split(" ", $id);
        print join(":", @ida)."\n";
        my $NewId = $ida[0];
        print ">$NewId\t";

        #my $s = "GGTCCAGGGG";
        $GCcount1++ while $s =~ /[CG]/gi;
        my $GCNum = ($s =~ tr/GC/CG/);

        print "$GCcount1\t$GCNum";
        print "\n";

        push @faLens, $falen;
    }
}

close $SC;


print join(",", @faLens)."\n";





