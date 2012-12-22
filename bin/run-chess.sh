#!/bin/bash
# run-chess.sh -- created 2012-12-01, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

# ################ SETTINGS ##############
# Regenerate existing datasets
REGENERATE=false
PRUNE_OUTPUT_DIR=false

THIS_DIR=$(cd "$(dirname "$0")"; pwd)
UTILS_DIR="$THIS_DIR/utils"
DATASETS_DIR="$THIS_DIR/../datasets"
OUTPUT_DIR="$THIS_DIR/../output"
NOW=$(date +%Y%m%d-%H%M%S)

CHESS_GEN="$UTILS_DIR/py/chess-generator.py"
ALL_RUNNER="$THIS_DIR/run-all.sh"
OUTPUT="$OUTPUT_DIR/chess-benchmark-$NOW.csv"

Q=echo
Q=
# ################ End of SETTINGS ##############

function cmd_help() {
cat <<EOF
$0 <Dim> <Start> <Increment> <Stop>
 Run chess benchmark 
  - Dim       : chessboard dim X dim
  - Start     : Start number of points
  - Increment : Increment for each benchmark iteration
  - Stop      : Stop after generating the given number of points

EOF
}

if [ ! $# -eq 4 ]; then
    cmd_help
    exit -1
fi
DIM=$1
START=$2
INCR=$3
STOP=$4

if [ $PRUNE_OUTPUT_DIR == "true" ]; then
    rm $OUTPUT_DIR/* 2> /dev/null
fi

HEADER="Width,Height,Points,Tool,Trees,Features,LeavesMin,LeavesMean,LeavesMax,DepthMin,DepthMean,DepthMax,TrainSize,OOB,TestSize,ClassError"
echo $HEADER > $OUTPUT

for N in $(seq $START $INCR $STOP); do
DATASET="chess_${DIM}x${DIM}x$N"
PARAMS="${DIM},${DIM},$N,"
DATASET_DIR="$DATASETS_DIR/$DATASET"

if [ ! -d $DATASET_DIR -o $REGENERATE == "true" ]; then
    $Q $CHESS_GEN -x $DIM -y $DIM -p $N -o $DATASETS_DIR
fi

$Q cp $DATASETS_DIR/chess/rf.conf $DATASET_DIR/
$Q $ALL_RUNNER $DATASET "$PARAMS" "$HEADER" | tee -a $OUTPUT 

done
# vi: 
