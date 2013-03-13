#!/bin/bash

DATASET=$1
source "../../datasets/$DATASET/rf.conf"
echo $DATASET

TREES="5 10 25 50 100 200 500 1000"

OUTD="../../output/wise.io.$DATASET"
mkdir -p "$OUTD"
for TREE in $TREES; do
    OUTF="$OUTD/res_$TREE.txt"
	python ./run-rf.py  "$DATASET" --ntrees=$TREE --predictor=$(expr $RF_PRED_CLASS_IDX - 1) > "$OUTF"
	if [ ! -z "$2" ]; then 
		exit
	fi
done

