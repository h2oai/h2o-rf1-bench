#!/bin/bash

DATASET=$1
cat "../../datasets/$DATASET/rf.conf"
source "../../datasets/$DATASET/rf.conf"
echo $DATASET

TREES="5 10 25 50 100 200 500 1000"

OUTD="../../output/wise.io.$DATASET"
mkdir -p "$OUTD"
for TREE in $TREES; do
    OUTF="$OUTD/res_$TREE.txt"
	python ./run-rf.py  "$DATASET" --ntrees=$TREE --predictor=$(expr $RF_PRED_CLASS_IDX - 1) ${RF_COLUMN_IGNORES:+"--ignores=${RF_COLUMN_IGNORES}"} > "$OUTF"
	if [ ! -z "$2" ]; then 
		exit
	fi
done

(cd $OUTD; 
  echo "Trees,Features,Sample,TrainTime,TestTime,OOB,ClassError" > results.csv
  ls -1 res_*.txt | while read f; do tail -n 1 $f; done >> results.csv
  )
