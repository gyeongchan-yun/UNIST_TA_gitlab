#!/bin/bash

StudentFile=$1

REPODIR=""

prefix="uni"

while IFS= read -r username 
do
    sId=${username#${prefix}}
    echo ${sId}

    cd ${REPODIR}
    git clone 'Git URL as SSH' #Please make sure to activate the deployed key, use SSH not HTTP from git repository
    cd 'Change Directory to student directory'

    #git pull origin master # Because of some students may have modified something

    mkdir sp_assignment3
    cd sp_assignment3
    #copy assignment files to the repo

    git add ./
    git commit -m \"$2\"
    git push origin master
done < ${StudentFile}
