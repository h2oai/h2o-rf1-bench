#!/bin/bash
# find-leaves.sh -- created 2012-12-06, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

grep -e "Avg tree leaves" -e "Leaves summary" *.txt | sort | uniq | sed -e "s/-analysis-\(.*\)\.txt:/ \1: /"


# vi: 
