#!/bin/bash
# run-all.sh -- created 2012-11-30, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

THIS_DIR=$(cd "$(dirname "$0")"; pwd)
R_DIR="$THIS_DIR/R"
H2O_DIR="$THIS_DIR/h2o"
WEKA_DIR="$THIS_DIR/weka"

RUNNER="run-rf.sh"

function cmd_help() {
cat <<EOF
$0 <dataset> [<prefix>]
 Run R, h2o RandomForest implementation and store results
 
 - dataset : name of dataset to perform RF
 - prefix  : print prefix in front of each output line - typically parameters of dataset

EOF
}

if [ $# -lt 1 ]; then
    cmd_help
   exit -1
fi

RF_DS_NAME="$1"
PREFIX="$2"

#echo "*** Running R...."
R_OUTPUT_FILE="$(cd $R_DIR; "./$RUNNER" $RF_DS_NAME | tail -n 1 | sed -e 's/.*://' )"

#echo "*** Running H2O...." >2
H2O_OUTPUT_FILE="$(cd $H2O_DIR; "./$RUNNER" $RF_DS_NAME | tail -n 1 | sed -e 's/.*://')"

cat <<EOF
${PREFIX}R,$(tail -n 1 $R_OUTPUT_FILE)
${PREFIX}h2o,$(tail -n 1 $H2O_OUTPUT_FILE)
EOF
# vi: 
