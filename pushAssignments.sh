#!/bin/bash

StudentFile=$1
AssignmentFilePath=$2

COURSEDIR=""

while IFS= read -r sId
do
    cd $COURSEDIR/$sId
    git pull origin master # Because of some students may have modified something

    cp $2 ./
    git push origin master
done < ${StudentFile}
