CONF_DIR="$THIS_DIR/../../conf"
RF_CONF_FILE="$CONF_DIR/rf.conf"
NOW=$(date +%Y%m%d-%H%M%S)

function cmd_help() {
    echo "$0 <dataset>"
    echo "   Run RF with help of $TOOL"
    echo "   - dataset: name of existing dataset"
}

function check_datasets() {
    if [ ! -f $RF_TRAIN_DS ]; then
        echo "Training dataset $RF_TRAIN_DS does not exist!"
        cmd_help
        exit -1
    fi
    if [ ! -f $RF_TEST_DS ]; then
        echo "Testing dataset $RF_TEST_DS does not exist!"
        cmd_help
        exit -1
    fi
}

function parse_conf() {
    # Parse global RF configuration
    source $RF_CONF_FILE

    # Parse dataset local RF configuration
    if [ -f $RF_DS_CONF ]; then
        source $RF_DS_CONF
    fi
    # ### End of configuraiton ###
}

function print_conf() {
cat <<EOF
========================================================
RF configuration:
   Train dataset: $RF_TRAIN_DS
   Test dataset:  $RF_TEST_DS
   RF output:        $RF_OUTPUT_DIR

   Seed:          $RF_SEED
   Num of trees:  $RF_NTREES

   All RF variables:
$(set -o posix; set | grep "^RF_" | sed -e "s/^/        /")
========================================================
EOF
}
