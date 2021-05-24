#!/bin/bash
PROGRAM=$1
CURRENT_PATH=$2
rm $CURRENT_PATH"result.txt"
for t in $CURRENT_PATH"tests"/*.in
do
    myt="${t%.*}.test.out"
    echo $myt
    $PROGRAM < $t > $myt
    if cmp --silent "${t%.*}.out" $myt; then
        echo "OK" >> $CURRENT_PATH"result.txt"
    else
        echo "Wrong answer" >> $CURRENT_PATH"result.txt"
    fi
    rm $myt
done
