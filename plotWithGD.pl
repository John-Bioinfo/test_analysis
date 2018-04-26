use warnings;
use strict;
use GD::Graph::bars;
use GD::Graph::Data;
use GD::Graph;


my @data = ( 
  ["1st","2nd","3rd","4th","5th","6th","7th", "8th", "9th"],
  [    1,    2,    5,    6,    3,  1.5,    1,     3,     4],
  [ sort { $a <=> $b } (1, 2, 5, 6, 3, 1.5, 1, 3, 4) ]
);


my $graph = GD::Graph::bars->new(900, 700);

#$graph->set_title_font('/fonts/arial.ttf', 18);
#$graph->set_x_label_font('/fonts/arial.ttf', 16);
#$graph->set_y_label_font('/fonts/arial.ttf', 20);


$graph->set( 
    x_label           => 'X Label',
    y_label           => 'Y label',
    title             => 'Some simple graph',
    y_max_value       => 8,
    y_tick_number     => 8,
    y_label_skip      => 2 ,

) or die $graph->error;

my $font_file  = '/usr/share/fonts/dejavu/DejaVuSans.ttf';

$graph->set_title_font($font_file, 18);
$graph->set_x_label_font($font_file, 20);
$graph->set_y_label_font($font_file, 20);

$graph->set_x_axis_font($font_file, 12);
$graph->set_y_axis_font($font_file, 12);
# $graph->set_legend_font($font_file, 9);

# http://wellington.pm.org/archive/201002/grant-gd-graph/slide016.html
## https://metacpan.org/pod/GD::Graph
#

my $gd = $graph->plot(\@data) or die $graph->error;


open(IMG, '>file.png') or die $!;
binmode IMG;
print IMG $gd->png
