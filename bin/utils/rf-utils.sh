CONF_DIR="$THIS_DIR/../../conf"
RF_CONF_FILE="$CONF_DIR/rf.conf"
NOW=$(date +%Y%m%d-%H%M%S)

function cmd_help() {
    echo "$0 <dataset> [-conf <rf.conf>]"
    echo "   Run RF with help of $TOOL"
    echo "   <dataset>       : name of existing dataset"
    echo "   -conf <rf.conf> : load also given RF config file (override all other configurations)" 
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
    source "$RF_CONF_FILE"

    # Parse dataset local RF configuration
    if [ -f "$RF_DS_CONF" ]; then
        source "$RF_DS_CONF"
    fi

    # Parse local config file
    if [ -f "$RF_LOCAL_CONF" ]; then
        source "$RF_LOCAL_CONF"
    fi

    # Parse given config file
    for PARAM in "$@"; do
        case $PARAM in
            -conf) 
                shift
                LOCAL_CONF="$1"
                shift
                ;;
            -h2orng)
                shift
                RF_H2O_RNG="$1"
                shift
                ;;
            -sample)
                shift
                RF_SAMPLING_RATIO="$1"
                shift
                ;;
        esac
    done

    echo "Cmd line options:"
    echo "  LOCAL_CONF=$LOCAL_CONF"
    echo "  RF_H2O_RNG=$RF_H2O_RNG"
    echo "  RF_SAMPLING_RATIO=$RF_SAMPLING_RATIO"
    
    if [ -f "$LOCAL_CONF" ]; then
        source "$LOCAL_CONF"
    elif [ -n "$LOCAL_CONF" ]; then
        echo "File \"$LOCAL_CONF\" does not exist!"
        exit
    fi

    # ### End of configuraiton ###
}

function print_conf() {
#cat | tee "$RF_OUTPUT_RUNCONFG" <<EOF
cat > "$RF_OUTPUT_RUNCONFG" <<EOF
========================================================
RF configuration:
   Train dataset: $RF_TRAIN_DS
   Test dataset:  $RF_TEST_DS
   RF output:     $RF_OUTPUT_DIR

   Seed:          $RF_SEED
   Num of trees:  $RF_NTREES

   All RF variables:
$(set -o posix; set | grep "^RF_" | sed -e "s/^/        /")
========================================================
EOF
cat "$RF_OUTPUT_RUNCONFG"
}
