#!/bin/bash

# Get current branch name
prod_branch=$1
current="$(git rev-parse --abbrev-ref HEAD)"
echo "Current branch:"
echo $current
echo "Production branch:"
echo $prod_branch

if [ "$current" = "$prod_branch" ]
then
	echo "restarting server"
	git pull origin $current
	sleep 2 && pkill python3.6 &
	echo "Restarting server: $(date) on branch ($current)" >> ~/update.log
else
	echo "Not currect repo: $(date), expected $current but got $prod_branch"
fi
