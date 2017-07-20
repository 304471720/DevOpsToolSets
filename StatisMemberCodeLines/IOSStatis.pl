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
    if( $tmp =~ /(.*)\.(m|h)/)
    {
    	print "$tmp\n";
    }
}
