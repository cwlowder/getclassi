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
	echo "restarting file"
	git pull origin $current
fi
