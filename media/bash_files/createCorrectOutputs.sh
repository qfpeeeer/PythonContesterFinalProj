#!/bin/bash
PROGRAM=$1
CURRENT_PATH=$2
rm $CURRENT_PATH"result.txt"
for t in $CURRENT_PATH"tests"/*.in
do
    myt="${t%.*}.out"
    echo $myt
    $PROGRAM < $t > $myt
done
