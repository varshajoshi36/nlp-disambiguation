#! /usr/bin/perl -w 

use strict;
use warnings;

# Sample Perl program, showing how to use the
# WordNet::Similarity measures.

# WordNet::QueryData is required by all the
# relatedness modules.
use WordNet::QueryData;

# 'use' each module that you wish to use.

use WordNet::Similarity::random;
use WordNet::Similarity::lesk;

# Get the concepts.
my $wps1 = shift;
my $wps2 = shift;

unless (defined $wps1 and defined $wps2) {
    print STDERR "Undefined input\n";
    print STDERR "Usage: sample.pl synset1 synset2\n";
    print STDERR "\tSynsets must be in word#pos#sense format (ex., dog#n#1)\n";
    exit 1;
}

# Load WordNet::QueryData
print STDERR "Loading WordNet... ";
my $wn = WordNet::QueryData->new;
die "Unable to create WordNet object.\n" if(!$wn);
print STDERR "done.\n";


# Create an object for each of the measures of
# semantic relatedness.

print STDERR "Creating lesk object... ";
my $lesk = WordNet::Similarity::lesk->new($wn, "config-files/config-lesk.conf");
die "Unable to create lesk object.\n" if(!defined $lesk);
my ($error, $errString) = $lesk->getError();
die $errString if($error > 1);
print STDERR "done.\n";

# Find the relatedness of the concepts using each of
# the measures.

my $value = $lesk->getRelatedness($wps1, $wps2);
($error, $errString) = $lesk->getError();
die $errString if($error > 1);

print "LESK Similarity = $value\n";
print "LESK ErrorString = $errString\n" if $error;

__END__

