#!/bin/bash



message=$1



echo $message

git add *
git commit -a -m "$message"
git push
