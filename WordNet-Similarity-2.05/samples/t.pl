use WordNet::QueryData;
use WordNet::Tools;
$wps1 = shift;
my $wn = WordNet::QueryData->new;
my $wntools = WordNet::Tools->new($wn);
my $wnHashCode = $wntools->hashCode();
my $newstring = $wntools->compoundify($wps1);
print "$newstring\n"
