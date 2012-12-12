#!/bin/bash
# find-leaves.sh -- created 2012-12-06, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

grep -e "Tree leaves" -e "Leaves" *.txt | sort | uniq | sed -e "s/-analysi.*:/:/"


# vi: 
