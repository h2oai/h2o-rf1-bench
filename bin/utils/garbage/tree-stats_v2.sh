#!/bin/bash
OUT=h2o-covtype-analysis-20121226-172210.txt
cnt=1
rm -rf tree.txt
grep "Tree :" $OUT | while read tree; do
    echo -ne "\n Tree $cnt," >> tree.txt
    echo "$tree" | sed -e "s/A/\nA/g" | grep "<" | sed "s/\([^ ]*\) .*/\1/" | sort | uniq -c | sort -nr | head -n 20 | sed -e "s/^ *//" | tr "\\n" ","  >> tree.txt
    cnt=`expr $cnt + 1`
done
