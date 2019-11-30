#!/bin/sh

if [[ $(id -u) -ne 0 ]] ; then
    echo "Need to be root"
    exit 1
fi

result=$(git diff | grep "^+" | wc -l)
echo $result "lines added"

if [ $result < 10 ]
then
	echo "Less number, stopping"
fi

echo "Going ahead"

git diff | grep "^+" | cut -c2- > data/input.log
echo "$(tail -n +2 input.log)" > data/input.log

git commit -am "123"

sudo bash upload.sh neo4j deven123 data/input.log

echo "Upload complete"
