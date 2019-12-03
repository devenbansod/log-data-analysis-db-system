#!/bin/bash

if [[ $(id -u) -ne 0 ]] ; then
    echo "Need to be root"
    exit 1
fi

LOCKDIR=".lock"
MIN_NUM_FILES=20

# Remove the lock directory
function cleanup {
    if rmdir $LOCKDIR; then
        echo "Finished"
    else
        echo "Failed to remove lock directory '$LOCKDIR'"
        exit 1
    fi
}

if mkdir $LOCKDIR; then
    # Ensure that if we "grabbed a lock", we release it
    # Works for SIGTERM and SIGINT(Ctrl-C)
    trap "cleanup" EXIT
    echo "Acquired lock, running"

    inside_git_repo="$(git rev-parse --is-inside-work-tree 2>/dev/null)"
    if [ "$inside_git_repo" ]; then
      echo "inside git repo"
    else
      echo "not in git repo"
      git init
    fi

    result=$(git diff being-watched.log | grep "^+" | wc -l)
    echo $result "lines added"

    # turn it into integers
    result=$(($result+0))
    MIN_NUM_FILES=$(($MIN_NUM_FILES+0))
    if (($result < $MIN_NUM_FILES));
    then
        echo "Less number of lines, stopping!"
        exit
    fi

    # get the new logs
    git diff being-watched.log | grep "^+" | cut -c2- > data/input.log
    echo "$(tail -n +2 data/input.log)" > data/input.log

    # commit these changes
    commitmsg=$(date +%Y%m%d%H%M%S)
    git commit -am "Run completed on $commitmsg"

    # run the reduction and data ingestion script
    sudo bash upload.sh neo4j $PASS data/input.log

    echo "Upload complete, commit added"
else
    echo "Could not create lock directory '$LOCKDIR'"
    exit 1
fi
