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
my ($i,$j,$k,$f);
$i = 0;
$j= 0;
$k = 0;
$f = 0;	
print "wps1 = $wps1\n";
my $totalcount;
my @flg_frm_py;
$totalcount = 0;
@split_list1 = split(/,/,$wps1);
$arrs1 = @split_list1;
$split_list1[$i] =~ s/\[//ig;
$split_list1[$arrs1-1] =~ s/\]//ig;
for($i = 0; $i < $arrs1; $i = $i+1){
		$split_list1[$i] =~ s/\[//ig;
	$split_list1[$i] =~ s/\'//ig;
	$split_list1[$i] =~ s/\ //ig;
	if($split_list1[$i]eq'%+') 
	{
		$list_size[$j] = $k;
		$j =$j + 1;
		$totalcount = $totalcount + $k;
		$k = 0;
		
	}
	elsif ($split_list1[$i]eq'%$#')
	{
		$flg_frm_py[$f] = $split_list1[$i + 1];
		$f = $f + 1;
	}
	else {
		$lists[$j][$k] = $split_list1[$i];
		$k = $k + 1;
	}
		
}

print "Split_list:@split_list1\n";
#print "Total count = $totalcount\n"; 
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
	print "\n";
	for($k = 0;$k < $list_size[$j]; $k++){
		print "$lists[$j][$k]";
	}
}
for ($j = 0; $j < $no_of_target_words; $j = $j + 1){
	$flag_list[$j] = "0";
}
$j = 0;
my $lesk = WordNet::Similarity::lesk->new($wn, "config-files/config-lesk.conf");
die "Unable to create lesk object.\n" if(!defined $lesk);
($error, $errString) = $lesk->getError();
die $errString if($error > 1);
print"\n";
while ($j < $no_of_target_words){
	$k = 0;
	while($k < $list_size[$j]){
		for ($i = $k + 1; $i < $list_size[$j]; $i = $i+1){
			#print "$lists[$j][$k]\t $lists[$j][$i]\n";
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
print "Flag_list = @flag_list\n";
my $h;
#for all flagged arrays take 2 arrays before and after that array for consideration and resolve for sense  
$j = 0;
$i = 0;
$k = 0;
my @freq_list;
my ($a,$b);
$a = 0;
my $maxsyn_count;
$maxsyn_count = 2;
my ($maxval,$maxsyn1,$maxsyn2);
#output contains the top synsets,max similarity and window size 
my @output;
$maxval = 0;
my @win;
my $win_size;
#maxsim variable is to identify the synset for which max similarity is given in its window
my $maxsim;
#this synset is one which is allocated to the polysemeous word
my $maxsyn;
#o_flag is to recognize if the maxsyn is same for any of the two comparisons in the window of the target word
my $o_flag;
$o_flag = 0;
#print "\nno_of_target_words = $no_of_target_words\n";
while ($j < $no_of_target_words){
	if($flag_list[$j] == 1){
		
		$maxsim = 0;
		#print "List Size = $list_size[$j]\n\n";
		if($j eq 0){
			if($no_of_target_words eq 1){
				print "only one target word\n";
				last;
			}
			if($no_of_target_words eq 2){
				push(@win,$j+1);
			}
			else{
				push(@win,$j+1);
				push(@win,$j+2);
			}
		}
		if($j eq 1){
			if($no_of_target_words eq 2){
				push(@win,$j-1);
			}
			if($no_of_target_words eq 3){
				push(@win,$j-1);
				push(@win,$j+1);
			}
			elsif($no_of_target_words gt 3){
				push(@win,$j-1);
				push(@win,$j+1);
				push(@win,$j+2);
			}
		}
		if($j gt 1){
			push(@win,$j-1);
			push(@win,$j-2);
			if(($no_of_target_words-1) le $j){
			
			}
			elsif(($no_of_target_words-1) eq ($j+1)){
				push(@win,$j+1);
			}
			else {
				push(@win,$j+1);
				push(@win,$j+2);
			}
			
		}
		$win_size = @win;
		#print "Window[$j] : @win\t $win_size ";
		for($i = 0; $i < $win_size; $i = $i + 1){
			
			$maxval = 0;
			$h = 0;
			$k = 0;
			while($k <  $list_size[$j]){
				
				while ($h < $list_size[$win[$i]]){
					#print "$k = $lists[$j][$k]\t $lists[$win[$i]][$h]\n ";
					$value = $lesk->getRelatedness($lists[$j][$k],$lists[$win[$i]][$h]);
					($error, $errString) = $lesk->getError();
					die $errString if($error > 1);
					if($value > $maxval){
						$maxval = $value;
						$maxsyn1 = $lists[$j][$k];
						$maxsyn2 = $lists[$win[$i]][$h];
						
						
					}
					$h = $h + 1;
				}
				
				$k = $k + 1;
				$h = 0;
			}
			if($maxsim eq $maxval ){
				$o_flag = 1;
			}
			if ($maxsim < $maxval){
				$maxsim = $maxval;
				$maxsyn = $maxsyn1;
			}
			
			
			
		}			
	
	
		if($o_flag eq 0) {
			my ($wps1gloss, $wps2gloss, $weight, $relation ) = $obj -> getSuperGlosses ($maxsyn, $maxsyn2);
			print "$maxsyn:";
			print "$wps1gloss->[0]\n";
			push(@output,$maxsyn);
		}
	}
	$j = $j + 1;
	for($i = 0; $i < $win_size;$i = $i + 1){
		delete $win[$i];
	}
	$o_flag = 0;
	$win_size = @win;
}

my $frq_list_size;
$frq_list_size =@freq_list;
sub first_index {
	my @param_list = @_;
	my $param_size;
	$param_size = @param_list;
	my $search_q = $param_list[0];
	
	my $n;
	for($n = 1; $n < $param_size; $n = $n + 1){
		if($search_q eq $param_list[$n]){
			return ($n - 1);
		}
	}

}
sub count {
	my @param_list = @_;
	my $param_size;
	$param_size = @param_list;
	my $search_q = $param_list[0];
	my $cnt;
	$cnt = 0;
	my $n;
	for($n = 1; $n < $param_size; $n = $n + 1){
		if($search_q eq $param_list[$n]){
			$cnt = $cnt + 1;
		}
	}
	return $cnt;

}
my $freq_cnt;
print "Output to python = @output\n";
__END__

