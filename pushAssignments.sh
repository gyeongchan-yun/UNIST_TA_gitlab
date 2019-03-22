#!/bin/bash

function check_dir() {
    if [ ! -d $1 ] ; then
        echo "$1 : No such directory."
        exit 1;
    fi
}

StudentFile=$1

group=""  # gitlab group is a course
students_dir=""  # directory of all students project
check_dir ${students_dir}

assignment=""
check_dir ${assignment}

prefix="uni"

while IFS= read -r username 
do
    echo ${username}

    cd ${students_dir}
    git clone 'git@gitlab.com:'${group}'/'${username}'.git' # use SSH not HTTP from git repository
    cd ${username}
    check_dir ${username}  # check if git clone works

    git pull origin master # Because some students may have modified something

    cp -r ${assignment} . # copy assignment files to the repo

    git add ./
    git commit -m "ADD ${assignment}"
    git push origin master
done < ${StudentFile}
