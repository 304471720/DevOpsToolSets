#!/usr/bin/perl
use strict;
my $file_in = shift @ARGV;
open DEF, "< $file_in" or die "Can't open $file_in: $!";
local $/;
my $text = <DEF>;
close DEF; 
while ( $text =~ /RCS file(.*?)==/sg ) 
{
    my $tmp = $1;
    if( $tmp =~ /(.*)\.(java|xml|jsp|js)/)
    {
	if( $tmp =~ /revision 1.1\n(.*);/ )
	{
	   my $lines = $1;
	   #my $linechangesnum= ` cat $tmp |grep 'lines:' |awk '{print \$9+\$10}' `;
	   #my $linechangesnum= system("printf $tmp | grep 'lines:' |awk '{print \$9+\$10}' ");
	   my $linechangesnum=0;
	   while ( $tmp =~ /lines: (\+\d+) (\-\d+)/sg )
	   {
		$linechangesnum += $1 + $2 ;
	   }
	   print "$linechangesnum\n";
           if( $tmp =~ /author:/)
           {
               $tmp =~ /Working file: (.*)/;
               my $myfile = $1;
               #print "$myfile\n";
	       my $result = "";
	       if( -e $myfile)
	       {
                   $result =  `cat  $myfile | wc -l `;
	       }
               $result =~ s/[\r\n]$//;
	       $result += $linechangesnum; 
               #print  "  lines: +".$result." -".$result;
               $lines =~ s/(author: .*)/$1  lines: +$result -$result/;
	       $tmp =~ s/revision 1.1\n(.*);/revision 1.1\n$lines/;
               #print $tmp;
           }
	}
    	print "$tmp\n";
    }
}
