#! /usr/bin/perl -w 
use strict;
use warnings;
use WordNet::QueryData;
use WordNet::Similarity::GlossFinder;
use WordNet::Similarity::lesk;
use WordNet::Similarity::DepthFinder;
#get query formattes in python and send all the synsets of all words in an array
my $wps1;
my $arrs1;
$wps1 = shift;
unless ($wps1) {
    print STDERR "Undefined input\n";
    print STDERR "Usage: sample.pl synset_list \n";
    #print STDERR "\tSynsets must be in word#pos#sense format (ex., dog#n#1)\n";
    exit 1;
}
#format the input such that an array in perl will conatain arrays of synsets for indivisual word
my ($error, $errString);
my $err;
my @split_list1;
my @lists;
my @list_size;
my ($i,$j,$k);
$i = 0;
$j= 0;
$k = 0;	
my $totalcount;
$totalcount = 0;
@split_list1 = split(/,/,$wps1);
$arrs1 = @split_list1;
$split_list1[$i] =~ s/\[//ig;
$split_list1[$arrs1-1] =~ s/\]//ig;
for($i = 0; $i < $arrs1; $i = $i+1){
	$split_list1[$i] =~ s/\'//ig;
	$split_list1[$i] =~ s/\ //ig;
	if($split_list1[$i]eq'%$#') 
	{
		$list_size[$j] = $k;
		$j =$j + 1;
		$totalcount = $totalcount + $k;
		$k = 0;
		
	}
	else {
		$lists[$j][$k] = $split_list1[$i];
		$k = $k + 1;
	}
		
}
#print "\n\nSplit_list:@split_list1\n";
#print "Total count = $totalcount\n"; 
# Load WordNet::QueryData
my $wn = WordNet::QueryData->new;
die "Unable to create WordNet object.\n" if(!$wn);
#the following lines are for gloss def
my $obj = WordNet::Similarity::GlossFinder->new ($wn);
($err, $errString) = $obj->getError ();
$err and die $errString;

my $lesk = WordNet::Similarity::lesk->new($wn, "config-files/config-lesk.conf");
die "Unable to create lesk object.\n" if(!defined $lesk);
($error, $errString) = $lesk->getError();
die $errString if($error > 1);
print"\n";
my $no_lists;
$no_lists = $j;
my ($value, $maxval);
$maxval = 0;
my @value_array;
for($i = 0; $i < $no_lists; $i = $i + 1){
	for($j = 1;$j < $list_size[$i]; $j = $j + 1){
		if($lists[$i][$j] eq '+%'){
			push(@value_array,$maxval);
			#push(@value_array,'+@');
			$maxval = 0;
		}
		else{
		      $value = $lesk->getRelatedness($lists[$i][0],$lists[$i][$j]);
		      if ($value > $maxval){
		      	$maxval = $value
		      }
		}
	}
	push(@value_array,'+@');
}
print "val array = @value_array\n";


























__END__
