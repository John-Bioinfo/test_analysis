=head2 Tm()

Title : Tm()
    Usage : $tm = $primer->Tm(-salt=>'0.05')
    Function: Calculates and returns the Tm (melting temperature) of the primer
    Returns : A scalar containing the Tm.
Args : -salt set the Na+ concentration on which to base the calculation.
      (A parameter should be added to allow the oligo concentration to be set.)

Notes : Calculation of Tm as per Allawi et. al Biochemistry 1997 36:10581-10594. Also see
    documentation at http://biotools.idtdna.com/analyzer/ as they
    use this formula and have a couple nice help pages. These Tm values will be about
    are about 0.5-3 degrees off from those of the idtdna web tool. I don't know why.
=cut

sub Tm {
    my ($self, %args) = @_;
    my $salt_conc = 0.05;           #salt concentration (molar units)
    my $oligo_conc = 0.00000025;    #oligo concentration (molar units)
    if ($args{'-salt'}) {$salt_conc = $args{'-salt'}} #accept object defined salt concentration
    #if ($args{'-oligo'}) {$oligo_conc = $args{'-oligo'}} #accept object defined oligo concentration
    my $seqobj = $self->seq();
    my $length = $seqobj->length();
    my $sequence = uc $seqobj->seq();
    my @dinucleotides;
    my $enthalpy;
    my $entropy;
    #Break sequence string into an array of all possible dinucleotides
    while ($sequence =~ /(.)(?=(.))/g) {
        push @dinucleotides, $1.$2;
    }
    #Build a hash with the thermodynamic values
    my %thermo_values = ('AA' => {'enthalpy' => -7.9,
            'entropy' => -22.2},
        'AC' => {'enthalpy' => -8.4,
            'entropy' => -22.4},
        'AG' => {'enthalpy' => -7.8,
            'entropy' => -21},
        'AT' => {'enthalpy' => -7.2,
            'entropy' => -20.4},
        'CA' => {'enthalpy' => -8.5,
            'entropy' => -22.7},
        'CC' => {'enthalpy' => -8,
            'entropy' => -19.9},
        'CG' => {'enthalpy' => -10.6,
            'entropy' => -27.2},
        'CT' => {'enthalpy' => -7.8,
            'entropy' => -21},
        'GA' => {'enthalpy' => -8.2,
            'entropy' => -22.2},
        'GC' => {'enthalpy' => -9.8,
            'entropy' => -24.4},
        'GG' => {'enthalpy' => -8,
            'entropy' => -19.9},
        'GT' => {'enthalpy' => -8.4,
            'entropy' => -22.4},
        'TA' => {'enthalpy' => -7.2,
            'entropy' => -21.3},
        'TC' => {'enthalpy' => -8.2,
            'entropy' => -22.2},
        'TG' => {'enthalpy' => -8.5,
            'entropy' => -22.7},
        'TT' => {'enthalpy' => -7.9,
            'entropy' => -22.2},
        'A' => {'enthalpy' => 2.3,
            'entropy' => 4.1},
        'C' => {'enthalpy' => 0.1,
            'entropy' => -2.8},
        'G' => {'enthalpy' => 0.1,
            'entropy' => -2.8},
        'T' => {'enthalpy' => 2.3,
            'entropy' => 4.1}
    );
    #Loop through dinucleotides and calculate cumulative enthalpy and entropy values
    for (@dinucleotides) {
        $enthalpy += $thermo_values{$_}{enthalpy};
        $entropy += $thermo_values{$_}{entropy};
    }
    #Account for initiation parameters
    $enthalpy += $thermo_values{substr($sequence, 0, 1)}{enthalpy};
    $entropy += $thermo_values{substr($sequence, 0, 1)}{entropy};
    $enthalpy += $thermo_values{substr($sequence, -1, 1)}{enthalpy};
    $entropy += $thermo_values{substr($sequence, -1, 1)}{entropy};
    #Symmetry correction
    $entropy -= 1.4;
    my $r = 1.987; #molar gas constant
    my $tm = ($enthalpy * 1000 / ($entropy + ($r * log($oligo_conc))) - 273.15 + (12* (log($salt_conc)/log(10))));
    $self->{'Tm'}=$tm;

    return $tm;
}

## ref :https://bioperl-l.bioperl.narkive.com/IWZB2hR6/bio-seqfeature-primer-calculating-the-primer-tm
