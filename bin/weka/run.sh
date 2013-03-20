#!/bin/bash

DATASET=$1
source "../../datasets/$DATASET/rf.conf"
echo $DATASET

rm ../../output/weka-*

MTRIES="$RF_MTRY"
SAMPLES="67"
TREES="5 10 25 50 100 200 500 1000"
for TREE in $TREES; do
    cat >rfl.conf  <<EOF
RF_NTREES=$TREE
EOF
	./run-rf.sh  "$DATASET" -conf rfl.conf
    sleep 2
	if [ ! -z "$2" ]; then 
		exit
	fi
done

mkdir ../../output/weka_$DATASET
mv ../../output/weka-$DATASET-* ../../output/weka_$DATASET
