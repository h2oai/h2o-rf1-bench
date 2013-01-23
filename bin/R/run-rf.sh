#!/bin/bash

# ### R configuration ###
THIS_DIR=$(cd "$(dirname "$0")"; pwd)
RF_UTILS="$THIS_DIR/../utils/rf-utils.sh"
TREEPARSER="$THIS_DIR/../utils/py/r-treeparser.py"
TOOL="R"
EXT=""

source "$RF_UTILS"
# ### End of Configuration ###

if [ $# -lt 1 ]; then
    cmd_help
   exit -1
fi

RF_DS_NAME="$1"
shift

# Parse configuraiton
parse_conf "$@"

# Check if datasets exist
check_datasets

# Print configuration
print_conf

#
# R-specific part
#
RF_SEED=42
RF_R_MTRY=$RF_MTRY

START_TIME=$(date +%s)
R --slave --no-save <<EOF
rf.ds.name   <- "$RF_DS_NAME"
${RF_R_SEED:+"rf.seed      <- $RF_R_SEED"}
rf.train.dsf <- "$RF_TRAIN_DS"
rf.test.dsf  <- "$RF_TEST_DS"
rf.ntrees    <- $RF_NTREES
rf.pred.class.idx  <- $RF_PRED_CLASS_IDX

rf.output.analysis <- "$RF_OUTPUT_ANALYSIS"
rf.output.trees    <- "$RF_OUTPUT_TREES"
rf.r.mtry          <- $RF_R_MTRY
rf.print.trees     <- $RF_PRINT_TREES
${RF_SAMPLING_RATIO:+"rf.sampling.ratio  <- $RF_SAMPLING_RATIO"}
$(cat rf.r)
EOF
END_TIME=$(date +%s)

if [ $RF_PRINT_TREES == "TRUE" ]; then
$Q $TREEPARSER -f $RF_OUTPUT_TREES > "$RF_OUTPUT_TREES.tmp"
mv "$RF_OUTPUT_TREES.tmp" "$RF_OUTPUT_TREES"
fi
cat $RF_OUTPUT_ANALYSIS

echo "Analysis is stored in:$RF_OUTPUT_ANALYSIS"
print_stats "$RF_OUTPUT_ANALYSIS"

