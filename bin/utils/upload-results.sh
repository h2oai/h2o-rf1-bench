#!/bin/bash

# ### Basic configuration ###
THIS_DIR=$(cd "$(dirname "$0")"; pwd)
RF_UTILS="$THIS_DIR/rf-utils.sh"
source "$RF_UTILS"
source "$RF_CONF_FILE"
# #### End of configuration ####

function get_dataset() {
    local filename=$1
    ds=$(echo $filename | sed -e "s/[^-]*-\(.*\)-analysis-.*/\1/")
    echo "$ds"
}

function get_tool() {
    local filename=$1
    tool=$(echo $filename | sed -e "s/\([^-]*\)-.*.txt/\1/")
    echo "$tool"
}

function get_time() {
    local filename=$1
    rundate=$(echo $filename | sed -e "s/.*-analysis-\(....\)\(..\)\(..\)-\(..\)\(..\)\(..\).txt/\1-\2-\3 \4:\5:\6/")
    echo "$rundate"
}

function get_data_prefix() {
    local filename=$1
    prefix=$(echo $filename | sed -e "s/\([^-]*\)-\(.*\)-analysis-\(....\)\(..\)\(..\)-\(..\)\(..\)\(..\).txt/\3-\4-\5 \6:\7:\8,\1,\2/")
    echo "$prefix"
}

function assertEq() {
    if [ "$1" != "$2" ]; then
        echo "$1 != $2"
        exit -1
    fi
}
function test_case1() {
    local TEST_DSNAME="h2o-chess_1x2x10000-analysis-20121218-235643.txt"

    assertEq "$(get_time "$TEST_DSNAME")" "2012-12-18 23:56:43"
    assertEq "$(get_tool "$TEST_DSNAME")" "h2o"
    assertEq "$(get_dataset "$TEST_DSNAME")" "chess_1x2x10000"
    assertEq "$(get_data_prefix "$TEST_DSNAME")" "2012-12-18 23:56:43,h2o,chess_1x2x10000"
}

function main() {
    tool="$1"
    find "$RF_OUTPUT_DIR" -maxdepth 1 -name "*-analysis-*" | sort | while read analysis_output; do
        process_analysis_output "$analysis_output"
    done
}

function process_analysis_output() {
    local ao="$1"
    local ao_file="$(basename "$ao")"
    local ao_prefix="$(get_data_prefix "$ao_file")"
    local ao_results="$(tail -n 1 "$ao")"

    echo "Processing file: $ao"
    echo " [Uploading row]>$ao_prefix,$ao_results"

    # call upload && mv "$ao" "$RF_SAVED_OUTPUT_DIR/" 
}

# Run simple test before running the core logic
test_case1
Q=echo
main "$@"
# vi: 
