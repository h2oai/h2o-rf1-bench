#!/bin/bash

# ### H2O configuration ###
THIS_DIR=$(cd "$(dirname "$0")"; pwd)
RF_UTILS="$THIS_DIR/../utils/rf-utils.sh"
TOOL="h2o"
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
# H2O-specific part
# 

CLASSPATH=h2o.jar
H2O_MAIN_CLASS=init.Boot

RF_H2O_JVM_ASSERTIONS=
JVM_PARAMS="${RF_H2O_JVM_ASSERTIONS} -Xmx${RF_H2O_JVM_XMX} -cp ${CLASSPATH} ${H2O_MAIN_CLASS}"
RF_PARAMS="-mainClass hex.rf.RandomForest -file $RF_TRAIN_DS -validationFile $RF_TEST_DS -ntrees $RF_NTREES -classcol $RF_PRED_CLASS_IDX_H2O ${RF_H2O_STAT_TYPE:+"-statType $RF_H2O_STAT_TYPE"} -seed $RF_SEED ${RF_H2O_BIN_LIMIT:+"-binLimit $RF_H2O_BIN_LIMIT"} ${RF_SAMPLING_RATIO:+"-sample $RF_SAMPLING_RATIO"} ${RF_H2O_RNG:+"-rng $RF_H2O_RNG"} ${RF_H2O_PARALLEL:+"-parallel $RF_H2O_PARALLEL"} ${RF_H2O_EXCLUSIVE_SPLIT_LIMIT:+"-exclusiveSplitLimit $RF_H2O_EXCLUSIVE_SPLIT_LIMIT"}  ${RF_H2O_VERBOSE_LEVEL:+"-verbose $RF_H2O_VERBOSE_LEVEL"} "

echo "H2O cmd parameters: $RF_PARAMS" | tee -a "$RF_OUTPUT_RUNCONFG"
echo "JVM cmd parameters: $JVM_PARAMS"| tee -a "$RF_OUTPUT_RUNCONFG"
echo -e "Cmd line:\njava $JVM_PARAMS $RF_PARAMS"

#Q=echo
$Q rm -rf /tmp/ice5*
$Q java $JVM_PARAMS $RF_PARAMS 2>&1 | tee ${RF_OUTPUT_ANALYSIS}.tmp | grep -v "^\[h2o\]" | grep -v "\[RF\]" | tee $RF_OUTPUT_ANALYSIS | cut -b -200
h2o_get_run_stats "$RF_OUTPUT_ANALYSIS" >> "$RF_OUTPUT_ANALYSIS"
#cat "$RF_OUTPUT_ANALYSIS"
echo "Analysis is stored in:$RF_OUTPUT_ANALYSIS"
echo -e "Cmd line:\njava $JVM_PARAMS $RF_PARAMS"
print_stats "$RF_OUTPUT_ANALYSIS"

