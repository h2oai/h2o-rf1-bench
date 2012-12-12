#!/bin/bash
# run-rf.sh -- created 2012-11-24, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

THIS_DIR=$(cd "$(dirname "$0")"; pwd)
DATASETS_DIR="$THIS_DIR/../../datasets"
Q=echo
Q=

function cmd_help() {
    echo "$0 <dataset> "
    echo "   convert dataset stored in datasets/<dataset>/R directory into ARFF format"
    echo "   dataset : name of dataset"
}

if [ ! $# -eq 1 ]; then
    cmd_help
   exit -1
fi

DATASET_DIR="$DATASETS_DIR/$1"
if [ ! -d $DATASET_DIR ]; then
    echo "Directory $DATASET_DIR does not exist!"
    cmd_help
    exit -1
fi

DATASET_R_DIR="$DATASET_DIR/R"
DATASET_WEKA_DIR="$DATASET_DIR/weka"

CONVERTOR="$THIS_DIR/generate-arff.sh"

TRAIN_FILE="$DATASET_R_DIR/train.csv"
TEST_FILE="$DATASET_R_DIR/test.csv"

if [ ! -f $TRAIN_FILE ]; then
    echo "File $TRAIN_FILE is missing!"
    exit -1
fi
if [ ! -f $TEST_FILE ]; then
    echo "File $TEST_FILE is missing!"
    exit -1
fi

WEKA_TRAIN_FILE="$DATASET_WEKA_DIR/train.csv.arff"
WEKA_TEST_FILE="$DATASET_WEKA_DIR/test.csv.arff"
WEKA_TMF_FILE="$DATASET_WEKA_DIR/tmp.arff"

$Q $CONVERTOR $TRAIN_FILE -o $DATASET_WEKA_DIR
$Q $CONVERTOR $TEST_FILE -o $DATASET_WEKA_DIR

# unify headers
cat > $WEKA_TMF_FILE <<EOF
$(sed "/@data/q" < $WEKA_TRAIN_FILE)
$(sed -e "H;/@data/h" -e '$g;$!d' < $WEKA_TEST_FILE | tail -n +2)
EOF

mv $WEKA_TMF_FILE $WEKA_TEST_FILE


