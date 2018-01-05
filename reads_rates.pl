#!/usr/bin/perl

use strict;
use warnings;
use File::Spec;
use File::Basename;
use Getopt::Std;
use Statistics::Basic qw(:all);
use List::Util qw(max min sum);
use Cwd 'abs_path';

#
#
#

my $version = "1.0";
my $argNum  = @ARGV;


my %rOpts = (a=>4, b=>2, c=>1, t=>5); 
my %inOpts;
getopts('a:b:c:o:d:n:p', \%inOpts);

die("
    perl Probe_stats.pl version $version by Zong-Yun QIAO (gulile\@yeah.net)

    Purpose:
    prepare data of Probe experiments for Machine learning

    Usage:

    perl Probe_stats.pl -d <DIR> -o <DIR> 

    Options (defaults in parentheses):
        -d <dir>
        -o <dir>
        -n <str>
        -a <float> log base of reads number
        -b <float> log base of rates
        -t <float> log base of low reads number
        -c <float> coefficient of rates standard deviation

") if ($argNum == 0);

foreach my $opt(keys %inOpts){
    # print "$opt\n $inOpts{$opt}\n";
    $rOpts{$opt} = $inOpts{$opt};
    if ($opt eq "o"){
        die("\'$inOpts{$opt}\' is not a correct out directory. Abort!\n") if(!(-d $inOpts{$opt}));
        print "Output directory: $rOpts{$opt}\n\n";
    } elsif ($opt eq "d"){
        die("\'$inOpts{$opt}\' is not a correct input directory. Abort!\n") if(!(-d $inOpts{$opt}));
        print "Input Data directory: $rOpts{$opt}\n\n";
    } elsif ($opt eq "p"){
        print "Software version is $version\n\n";
    }
}

my %probeData = ();       ## store all statistics results for each probe.

my $inDir = $rOpts{"d"};
my $outName = $rOpts{"n"};

my $readsBase = $rOpts{"a"};
my $rateBase = $rOpts{"b"};
my $ratesdCoef = $rOpts{"c"};
my $lowReadsBase = $rOpts{"t"};

## -------------------------------------------------------------------------------------------------
opendir(DIR, $inDir);

## Reads files in input Directory;
my $key;

while (my $file = readdir(DIR)){
    next if !($file =~ m/(Probe|Sample).(ontarget|Proberatio|reads).new.txt/);

    print "$inDir/$file...\n";

    open(my $FC, "$inDir/$file") or die $!;

    if ($file =~ m/.*?.ontarget.new.txt/){
        $key = "ontarget";
    } elsif ($file =~ m/.*?.Proberatio.new.txt/){
        $key = "pratio";
    } elsif ($file =~ m/.*?.reads.new.txt/) {
        $key = "reads";
    }

    my $probe;
    while(<$FC>){
        my $line = $_;
        chomp $line;
        chop($line) if ($line =~ m/\r$/);
        next if $line =~ m/^Sample|^Probe/;
        my @LineData = split /\t/, $line ;
        my $eleNum = @LineData;
        my @sampleData = @LineData[1 ... $eleNum-1];    # this is very import to assign its own data for each probe, use "my" in this line

        @sampleData = grep {$_ ne ""} @sampleData;    
        $probe  = $LineData[0] =~ s/_ontargetOfProbe|_ProbeRatio//gr;
        $probeData{$probe} -> {$key} = \@sampleData;
    }

    print "\n\n";
    close $FC;
}

my $Odir = $rOpts{"o"};

open(my $output, ">$Odir/".$outName."out_probeStats.xls") or die $!;

foreach my $probe (keys %probeData){

    printf $output ("%s",$probe);
    my ( $aveReads, $logaveReads );

    my ( $averates , $ratesStd ); 

    foreach my $key (keys %{$probeData{$probe}}){
        
        #  get data in the Hash, define mean of reasNum, mean of rates and stddev of rates ----
        my @raw_Data = @{$probeData{$probe} -> {$key}};

        ## ------------------------------------------------------------------------      ### rates data

        if ( &anyCont(@raw_Data) ){
            for(@raw_Data){s/%//g};
            my $rawNum = scalar @raw_Data;
            @raw_Data = sort { $a <=> $b } @raw_Data;

            my @data = @raw_Data[1 ... $rawNum-2];
            my $sampleN = scalar @data;
            my $sum = sum @data;

            my $Nums = join(",", @data);

            if ( $sampleN >=10 ) {
                $averates = $sum/$sampleN;
                $ratesStd = stddev(@data); 

            } else {
                $averates = 1.0;
                if ( $sampleN == 0 ) {
                    $ratesStd = 0;
                } else {
                    $ratesStd = stddev(@data);                                              
                #printf $output ("\tratio Fail");
                }
            }
        ## -----------------------------------------------------------------------    ###  reads data    
        } else {                                                  
            my $rawNum = scalar @raw_Data;
            @raw_Data = sort { $a <=> $b } @raw_Data;

            my @data = @raw_Data[1 ... $rawNum-2];
            my $sampleN = scalar @data;
            
            my $sum;
            if ( $sampleN ==0 ){
                $sum =0;
            
            } else {
                $sum = sum @data;
            }
            my $Nums = join(",", @data);
            
            $aveReads = $sum/($sampleN+1);
            if (  &all_2000(@data)  ){                                   ## reads number is below average level
                if ($aveReads == 0){
                    $logaveReads = 0;
                } else { 
                    $logaveReads = &logB($aveReads, $lowReadsBase );
                #printf $output ("\treads low-%s", $Nums);
                }
            } else {                                                     ## reads number is above average level
                $logaveReads = &logB($aveReads, $readsBase);

                #printf $output ("\treads high-%s", $Nums);
            }
        }

        #printf $output ("\t%s",$Nums);
    }

    my $logScore = &calcScore($logaveReads, $averates, $ratesStd);

    my $nScore = 0;
    if ($ratesStd == 0) {
        $nScore = 0;
    } else {
        $nScore = $aveReads * $averates / $ratesStd;
    }



    printf $output ("\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n", $aveReads, $averates, $ratesStd, $logScore, $nScore);
   
}

close $output;


sub anyCont{ $_ =~ m/%$/ && return 1 for @_; 0 }
sub all_100{ $_<=100 || return 0 for @_; 1 }
sub all_2000{ $_<2000 || return 0 for @_; 1 }

sub log10 {
   my $n = shift;
   return log($n)/log(10);
}


sub logB {
   my $n = shift;
   my $b = shift;
   return log($n)/log($b);
}


sub calcScore {
    my $logRead = shift;
    my $Rate = shift;
    my $sdRate = shift;
    if ($sdRate == 0){
        return 0;
    } else {
        return ($logRead + &logB($Rate, $rateBase))/ ($sdRate * $ratesdCoef) ;
    }
}


