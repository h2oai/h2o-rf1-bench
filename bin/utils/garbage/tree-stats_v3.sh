#!/bin/bash
OUT=h2o-covtype-analysis-20121226-172210.txt
cnt=1
TREECSV=tree-v3.csv
rm -rf "$TREECSV"
grep "Tree :" $OUT | while read tree; do
    echo -ne "\n Tree $cnt," >> tree.txt
    echo "$tree" | sed -e "s/A/\nA/g" | grep "<" | sed "s/\([^ ]*\) .*/\1/" | sort | uniq -c | sort -nr | sed -e "s/^ *//" | tr "\\n" ","  >> $TREECSV
    cnt=`expr $cnt + 1`
done
