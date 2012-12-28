#!/bin/bash

function get_tree_filename() {
    local n=$1
    if [ $n -lt 10 ]; then
        prefix="000"
    elif [ $n -lt 100 ]; then
        prefix="00"
    else
        prefix="0"
    fi

    echo "${prefix}${n}"
}

#OUT=h2o-covtype-analysis-20121226-172210.txt
OUT="$1"
if [ ! -f "$OUT" ]; then
    echo "File $OUT does not exist!"
    exit -1
fi

cnt=1
rm -rf tree_*.csv 2>/dev/null
echo "Parsing trees..."
grep "Tree :" $OUT | head -n 2| while read tree; do
    tree_fname="tree_$(get_tree_filename $cnt).csv"
    echo -ne "[${cnt}] "
    echo "$tree" | sed -e "s/A/\nA/g" | grep -e "<=" -e "==" | sed -e "s/\([^ ]*\) .*/\1/" -e "s/@/,/" | sed -e "s/\(^[^<=]*\)\([<=]\)/\1,\1\2/" | sort > "${tree_fname}"
    cnt=`expr $cnt + 1`
done

echo -e "\nDone"

echo -e "\nCollecting all split points..."
cat tree_0*.csv | cut -f 1 -d, |  sort | uniq > tree_split_points.csv

echo "Unique split points: $(wc -l tree_split_points.csv)"
cnt=1
echo "Tree,SplitVar,SplitPoint,AffectedLeaves" > tree_sps_stats.csv
for sp in $(cat tree_split_points.csv); do
    echo -ne "[$cnt] "
    #spfp="tree_sp_$(echo "$sp" | sed -e "s/<=/_le_/").csv"
    grep "${sp}," tree_0*.csv | sed -e "s/\t/,/" -e "s/.csv: */,/" -e "s/ /,/" >> tree_sps_stats.csv
    cnt=`expr $cnt + 1`
done

echo -e "\nDone"
