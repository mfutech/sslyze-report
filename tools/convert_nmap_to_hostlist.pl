#!/usr/bin/perl -an
#
#
# Host: 192.168.192.168 (hostname.domaine.local)       Ports: 443/open/tcp//https///
#

	if ($_ =~ m%Host:\s(.*) \((.*)\).*Ports: ([0-9]+)/open%) {
		($ip,$ho, $po) = ($1,$2,$3);
		if ($ho =~ m%^[a-zA-Z]% ) { 
			print("$ho : $po\n");
		} else {
			print "$ip : $po\n"; 
		};
	} else { 
		0 && print "%%$1%% ##$2## $_"  
	}
