#!/bin/bash

function getBranch() {
	echo $(git status --branch --porcelain | head -n 1 | sed 's/## //')
}

git add .
savebranch="$(getBranch)"
git commit
git push l-i-p master

