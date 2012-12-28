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
grep "Tree :" $OUT | head -n 5 | while read tree; do
    tree_fname="tree_$(get_tree_filename $cnt).csv"
    echo "$tree" | sed -e "s/A/\nA/g" | grep "<" | sed "s/\([^ ]*\) .*/\1/" | sort | uniq -c | sort -nr | sed -e "s/^ *//" | nl > "${tree_fname}"
    cnt=`expr $cnt + 1`
done

for t in $(ls -1 tree_0*.csv); do
    if [ -f "tree_table.csv" ]; then
        echo -ne "\n$t," >> tree_table.csv
    else
        echo -ne "$t," >> tree_table.csv
    fi
    head -n 50 "$t" | cut -f 2 | tr "\\n" "," >> tree_table.csv
done

cat tree_0*.csv | cut -f 2 | cut -f 2 -d\ | sort | uniq > tree_split_points.csv

echo "Unique split points: $(wc -l tree_split_points.csv)"
cnt=1
echo "tree,ranking,num_of_usages,split" > tree_sps_stats.csv
for sp in $(cat tree_split_points.csv); do
    echo -ne "$cnt "
    #spfp="tree_sp_$(echo "$sp" | sed -e "s/<=/_le_/").csv"
    grep "${sp}$" tree_0*.csv | sed -e "s/\t/,/" -e "s/.csv: */,/" -e "s/ /,/" >> tree_sps_stats.csv
    cnt=`expr $cnt + 1`
done
