#!/bin/bash
# up.sh -- created 2012-12-01, <+NAME+>
# @Last Change: 24-Dez-2004.
# @Revision:    0.0

H2O_HOME=/home/michal/prg/projects/h20/repos/h2o-at-bitbucker
H2OJAR=$H2O_HOME/build/h2o.jar
echo "Building H2O in ${H2O_HOME}..."
if [ "$1" == "skipgit" ]; then
echo "Skipping git pull..."
( cd "$H2O_HOME"; ./build.sh build )
else
( cd "$H2O_HOME"; git pull && ./build.sh build )
fi

echo "Doing: cp $H2OJAR ."
if [ -f "$H2OJAR" ]; then
    stat --printf "%y\n" h2o.jar
    cp "$H2OJAR" .
else
    echo "File $H2OJAR does not exist"
fi

stat --printf "%y\n" h2o.jar
# vi: 
