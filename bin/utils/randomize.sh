#!/bin/bash
# randomize.sh -- created 2012-11-24, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

DATASET=$1
NL=$(tail -n +2 $DATASET | wc -l)

# Use of $TRAIN_FACTOR of data to TRAIN, rest use to validation
TRAIN_FACTOR="2 / 3"
NL_TRAIN=$(expr $NL \* $TRAIN_FACTOR )
NL_TEST=$(expr $NL - $NL_TRAIN)
TMPF="/tmp/TMP_$DATASET"
HEADER=$(head -n 1 $DATASET)

cat <<EOF
 Train factor: $TRAIN_FACTOR
 NL_TRAIN:     $NL_TRAIN
 NL_TEST:      $NL_TEST
 header:       $HEADER
EOF


tail -n +2 $DATASET | shuf > $TMPF
cat > "train.csv" <<EOF
$HEADER
$(head -n $NL_TRAIN $TMPF)
EOF
#echo 'cat $TMF | tail -n $NL_TEST  > "test-$DATASET"'
cat > "test.csv" <<EOF
$HEADER
$(tail -n $NL_TEST $TMPF)
EOF

cat > "header" <<EOF
$HEADER
EOF

rm $TMPF
# vi: 
