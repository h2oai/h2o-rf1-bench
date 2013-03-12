#!/bin/bash

DATASET=$1
source "../../datasets/$DATASET/rf.conf"
echo $DATASET

rm ../../output/h2o-*

MTRIES="$RF_MTRY"
SAMPLES="10 20 30 40 50 60 67 70 80 90 99"
TREES="5 10 25 50 100 200 500 1000"

for TREE in $TREES; do
  for SAMPLE in $SAMPLES; do
   for MTRY in $MTRIES; do
	./run-rf.sh  "$DATASET" -ntrees=$TREE -sample=$SAMPLE
	if [ ! -z "$2" ]; then 
		exit
	fi
   done
  done
done

mkdir ../../output/$DATASET
mv ../../output/h2o-$DATASET-* ../../output/$DATASET
