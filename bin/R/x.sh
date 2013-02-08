#!/bin/bash

SAMPLES="10 20 30 40 50 60 70 80 90 99"
TREES="10 25 50 75 100 150 200 250 300"

for TREE in $TREES; do
for SAMPLE in $SAMPLES; do
echo "Running TREE  =$TREE"
echo "Running SAMPLE=$SAMPLE"
NAME="covtype-runner-${TREE}tree-${SAMPLE}sample.r"
cat covtype-runner.r | sed -e "s/XXXTREEXXX/$TREE/g" -e "s/XXXSAMPLEXXX/$SAMPLE/g" > $NAME
R --slave --no-save -f "$NAME" &
done
echo "Sleeping for 100sec...."
sleep 100
done
