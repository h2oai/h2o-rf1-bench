#!/bin/bash

# ### R configuration ###
THIS_DIR=$(cd "$(dirname "$0")"; pwd)
RF_UTILS="$THIS_DIR/../utils/rf-utils.sh"
TOOL="weka"
EXT=".arff"

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
# weka-specific part
# 

#CLASSPATH=weka.jar
CLASSPATH=weka-modified.jar
RF_CLASS=weka.classifiers.trees.RandomForest

# -K 0    - number of features to consider 
# -S 71   - random seed for split
# -no-cv  - no cross validation
# -I 5    - number trees to build
# -depth 0 - depth of tree (0=unlimited)
# -num-slots 1 - number of execution slots (1=no paralelism)
# -i
# -k 
# -I 5 - number of trees to build
# -print - print individual trees on output
# -c     - index of class attribute 
WEKA_JVM_PARAMS="-Xmx2048M"
RF_PARAMS="-K ${RF_WEKA_MTRY-0} -S $RF_SEED -I $RF_NTREES -c $RF_PRED_CLASS_IDX -num-slots 1 -k -i -D"
if [ $RF_PRINT_TREES == "TRUE" ]; then
    RF_PARAMS="$RF_PARAMS -print"
fi

# Prepare datasets
#$Q java -cp $CLASSPATH weka.core.converters.CSVLoader $TRAIN_DATASET > $TRAIN_DATASET_ARFF
#$Q java -cp $CLASSPATH weka.core.converters.CSVLoader $TEST_DATASET > $TEST_DATASET_ARFF
$Q java $WEKA_JVM_PARAMS -cp $CLASSPATH $RF_CLASS $RF_PARAMS -t $RF_TRAIN_DS -T $RF_TEST_DS > $RF_OUTPUT_ANALYSIS
cat $RF_OUTPUT_ANALYSIS
echo "Analysis is stored in:$RF_OUTPUT_ANALYSIS"
