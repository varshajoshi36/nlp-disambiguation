# This -*- perl -*- script writes the Makefile for WordNet::Similarity
# (Last updated $Id: Makefile.PL,v 1.44 2008/04/11 12:53:12 sidz1979 Exp $)
#
# Generates the Makefile for the WordNet::Similarity CPAN modules.
#
# ----------------------------------------------------------------------------

use 5.005;
use ExtUtils::MakeMaker;
use strict;

# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.

my $short_tests = 't/access.t t/res.t t/lin.t t/jcn.t t/path.t t/lch.t t/wup.t t/lesk.t t/vector_pairs.t t/vector.t t/hso.t t/random.t t/wn30loop.t t/config/rootnode.t';
my $long_tests = 't/*.t t/config/*.t t/utils/*.t';
my $opt_WNHOME;
my @programs_to_install = qw(BNCFreq.pl brownFreq.pl compounds.pl
                             rawtextFreq.pl semCorRawFreq.pl semCorFreq.pl
                             similarity.pl  treebankFreq.pl wordVectors.pl
                             wnDepths.pl similarity_server.pl);

# Get the WNHOME option from the command line
my @tmpArgs = @ARGV;
@ARGV = ();
foreach my $arg (@tmpArgs)
{
  if($arg =~ /^WNHOME=(.*)/)
  {
    $opt_WNHOME=$1;
  }
  else
  {
    push(@ARGV, $arg);
  }
}

# Write out the make file
WriteMakefile('NAME'         => 'WordNet::Similarity',
              'PREREQ_PM'    => {'WordNet::QueryData' => '1.40',
                                 'Text::Similarity'   => '0.02',
                                 'Digest::SHA1'       => '0',
                                 'File::Spec'         => '0',
                                 'File::Find'         => '0',
                                 'File::Temp'         => '0',
                                 'Getopt::Long'       => '0',
                                 'CGI'                => '0',
                                 'IO'                 => '0'},
              'PL_FILES'     => {'build/Infocontent.PL' => '$(INST_LIB)/WordNet/ic-semcor.dat',
                                 'build/Depthfiles.PL'  => '$(INST_LIB)/WordNet/synsetdepths.dat'},
              'CONFIGURE'    => \&configSub,
              'VERSION_FROM' => 'lib/WordNet/Similarity.pm',
              'EXE_FILES'    => [ map "utils/$_", @programs_to_install ],
              'dist'         => {'COMPRESS' => 'gzip -9f', 'SUFFIX' => 'gz'},
              'realclean'    => {'FILES' => 'build/wnpath.txt'},
              ($] >= 5.005 ?
               ('ABSTRACT_FROM'   => 'lib/WordNet/Similarity.pm',
                'AUTHOR'          => 'Ted Pedersen, Siddharth Patwardhan, Satanjeev Banerjee, Jason Michelizzi') : ()
              ),
              ($ExtUtils::MakeMaker::VERSION ge '6.30_00' ?
               ('LICENSE'         => 'gpl') : ()
              ),
              'NO_META'      => 'true'
             );

print STDERR <<"EOIN";

*** IMPORTANT NOTE: A number of default data files (information content
files, depth files, etc.) will be generated during this installation.
Some of these files require WordNet to be installed and accessible
through the WordNet::QueryData Perl module. This is typically done
by defining the WNHOME environment variable (specifying the WordNet
installation directory). Alternatively, the WNHOME option can specified
to Makefile.PL.

In addition, this means that the data files generated during the
installation depend on the version of WordNet currently installed on
your system. If at a later date, a newer version of WordNet is installed,
these data files should be regenerated by running this installation
again.

To continue the installation process run:

    make
    make test
    make install

You may also run a series of more rigorous tests by running 'make test_all'
instead of 'make test'.

EOIN

# Config subroutine called by MakeMaker
# Only saves the WNPATH (to be used during make), if provided
# on the command line.
sub configSub
{
  # Check if path to WordNet has been provided... If so... save it.
  if(defined $opt_WNHOME)
  {
    open(WNPATH, ">build/wnpath.txt") || die "Unable to open file for writing (internal error).\n";
    print WNPATH "$opt_WNHOME\n";
    close(WNPATH);
  }
  return {};
}

# What follows is some magic that makes some low-level modifications to
# the text that is about to be written to the Makefile.  We have to put
# this in the MY package so that the call to SUPER works correctly. The
# documentation for ExtUtils::MakeMaker has information on what we're
# actually doing here under the section 'Overriding MakeMaker Methods'.

# Essentially, we override MakeMaker's test() method and insert some
# extra text to add a new target, test_all.

package MY;

# override test() method to add a new target, test_all
sub test
{
  my $self = shift;
  my $text = $self->SUPER::test (@_);

  # here we make a copy of the Makefile portion made by SUPER::test(),
  # and then use the copy to make our own rule: test_all
  my $newtext = $text;
  $newtext =~ s/test(?!_harness)/test_all/g;
  $newtext =~ s/TEST/TEST_ALL/g;

  # don't forget the /m modifier:
  $newtext =~ s/(?<=TEST_ALL_FILES = ).*$/${long_tests}/m;

  $text .= $newtext;

  return $text;
}

# override the special_targets method to add test_all to the list of
# phony targets
sub special_targets
{
  my $self = shift;

  my $str = $self->SUPER::special_targets (@_);

  # add test_all to the list of phony targets
  $str =~ s/(\.PHONY:.* test\b)/$1 test_all/;

  return $str;
}
