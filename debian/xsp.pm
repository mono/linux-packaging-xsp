#!/usr/bin/perl
# debhelper sequence file for xsp scripts

use warnings;
use strict;
use Debian::Debhelper::Dh_Lib;

# have to use dh_installdeb as those scripts need to run for
# binary-arch and binary-indep packages
insert_before("dh_installdeb", "dh_installxsp");

1;
