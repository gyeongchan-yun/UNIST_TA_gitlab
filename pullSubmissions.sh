#!/bin/bash

StudentFile=$1

COURSEDIR=""

while IFS= read -r sId
do
    cd $COURSEDIR/$sId
    git pull origin master
done < ${StudentFile}
