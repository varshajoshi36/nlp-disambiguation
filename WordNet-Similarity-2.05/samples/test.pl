#! /usr/bin/perl -w 

use strict;
use warnings;

my @array = shift;                                            

for $elem (@array) {
    print $elem."\n";
}

__END__
