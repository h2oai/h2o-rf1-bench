#!/bin/bash

# ### R configuration ###
THIS_DIR=$(cd "$(dirname "$0")"; pwd)
RF_UTILS="$THIS_DIR/../utils/rf-utils.sh"
TREEPARSER="$THIS_DIR/../utils/py/r-treeparser.py"
TOOL="R"
EXT=""

source "$RF_UTILS"
# ### End of Configuration ###

if [ ! $# -eq 1 ]; then
    cmd_help
   exit -1
fi

RF_DS_NAME="$1"

# Parse configuraiton
parse_conf

# Check if datasets exist
check_datasets

# Print configuration
print_conf

#
# R-specific part
# 


R -q --no-save <<EOF
rf.ds.name   <- "$RF_DS_NAME"
rf.seed      <- $RF_SEED
rf.train.dsf <- "$RF_TRAIN_DS"
rf.test.dsf  <- "$RF_TEST_DS"
rf.ntrees    <- $RF_NTREES
rf.pred.formula    <- $RF_PRED_FORMULA
rf.pred.class.name <- "$RF_PRED_CLASS_NAME"

rf.output.analysis <- "$RF_OUTPUT_ANALYSIS"
rf.output.trees    <- "$RF_OUTPUT_TREES"
rf.r.mtry          <- $RF_R_MTRY
rf.print.trees     <- $RF_PRINT_TREES
${RF_SAMPLING_RATIO:+"rf.sampling.ratio  <- $RF_SAMPLING_RATIO"}
$(cat rf.r)
EOF

if [ $RF_PRINT_TREES == "TRUE" ]; then
#$Q $TREEPARSER -f $RF_OUTPUT_TREES > "$RF_OUTPUT_TREES.tmp"
#mv "$RF_OUTPUT_TREES.tmp" "$RF_OUTPUT_TREES"
fi
cat $RF_OUTPUT_ANALYSIS
echo "Analysis is stored in:$RF_OUTPUT_ANALYSIS"
