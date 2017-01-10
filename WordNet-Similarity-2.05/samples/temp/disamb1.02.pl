#! /usr/bin/perl -w 
use strict;
use warnings;

use WordNet::QueryData;
use WordNet::Similarity::GlossFinder;
use WordNet::Similarity::lesk;






#for all flagged arrays take 2 arrays before and after that array for consideration and resolve for sense  





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

@split_list1 = split(/,/,$wps1);
$arrs1 = @split_list1;
$split_list1[$i] =~ s/\[//ig;
$split_list1[$arrs1-1] =~ s/\]//ig;
for($i = 0; $i < $arrs1; $i = $i+1){
	$split_list1[$i] =~ s/\'//ig;
	$split_list1[$i] =~ s/\ //ig;
	
	if($split_list1[$i]eq'%+') 
	{
		$list_size[$j] = $k;
		$j =$j + 1;
		$k = 0;
	}
	else {
		$lists[$j][$k] = $split_list1[$i];
		$k = $k + 1;
	}
		
}

#in $j we hav number of lists
# Load WordNet::QueryData

my $wn = WordNet::QueryData->new;
die "Unable to create WordNet object.\n" if(!$wn);



#the following lines are for gloss def
my $obj = WordNet::Similarity::GlossFinder->new ($wn);
($err, $errString) = $obj->getError ();
$err and die $errString;

#Resolve all the words for polysemy if polysemous flag the array containing all synsets for that word as 
my $no_of_target_words;
my $size_of_current_arr;
$no_of_target_words = $j;
$j = 0;
my $value;
my @flag_list;
for ($j = 0; $j < $no_of_target_words; $j = $j + 1){
	$flag_list[$j] = "0";
}
$j = 0;
my $lesk = WordNet::Similarity::lesk->new($wn, "config-files/config-lesk.conf");
die "Unable to create lesk object.\n" if(!defined $lesk);
($error, $errString) = $lesk->getError();
die $errString if($error > 1);

while ($j < $no_of_target_words){
	$k = 0;
	while($k < $list_size[$j]){
		for ($i = $k + 1; $i < $list_size[$j]; $i = $i+1){
			
			$value = $lesk->getRelatedness($lists[$j][$k], $lists[$j][$i]);
			if ($value < 100)
			{
				$flag_list[$j] = "1";
				$i = $list_size[$j]; #to break the loop on detection 
			}
		}		
			$k = $k + 1;
	}
	$j = $j + 1;	
}
print "\n";
print @flag_list;
__END__

