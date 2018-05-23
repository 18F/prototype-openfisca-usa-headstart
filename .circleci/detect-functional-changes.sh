#! /usr/bin/env bash

IGNORE_DIFF_ON="README.md CONTRIBUTING.md .gitignore .circleci/* .github/*"

last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit

if git diff-index --name-only --exit-code $last_tagged_commit -- . `echo " $IGNORE_DIFF_ON" | sed 's/ / :(exclude)/g'`
then echo "No functional changes detected."
else
  echo "The functional files above were changed."
  exit 1
fi
