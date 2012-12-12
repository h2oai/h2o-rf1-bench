#!/bin/bash
# run-rf.sh -- created 2012-11-24, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

THIS_DIR=$(cd "$(dirname "$0")"; pwd)
WEKA_DIR="$THIS_DIR/..//weka"

function cmd_help() {
    echo "$0 <file_name> [-o dir]"
    echo "   CVS to ARFF convertor"
    echo "   file_name  : name of existing CVS file"
    echo "   -o dir     : output dir (. by default)"
}

if [ $# -lt 1 ]; then
    cmd_help
   exit -1
fi

INPUT="$1"
if [ ! -f $INPUT ]; then
    echo "File $INPUT does not exist!"
    cmd_help
    exit -1
fi

shift
if [ "$1" == "-o" ]; then
    shift
    OUTPUT_DIR="$1"
fi

if [ "$OUTPUT_DIR" != "" ]; then
    if [ ! -d $OUTPUT_DIR ]; then
        mkdir -p $OUTPUT_DIR
    fi
else
    OUTPUT_DIR="."
fi

CLASSPATH="$WEKA_DIR/weka.jar"
TRANS_CLASS=weka.core.converters.CSVLoader

#
OUTPUT="$OUTPUT_DIR/$(basename $INPUT).arff"
Q=echo
Q=

PARAMS='-M NA' # the second column contains nominal value

echo "Input file:  $INPUT"
echo "Output file: $OUTPUT"
echo "Parameters:  $PARAMS"
echo

# Prepare datasets
$Q java -cp $CLASSPATH $TRANS_CLASS $PARAMS $INPUT > $OUTPUT

# vi: 
